#!/usr/bin/env python3
"""
validate_schema.py

Purpose
-------
Validate analysis tables (e.g., call_level_table, session_summary_table, mouse_summary_table)
against a declarative schema file (YAML). Designed for reproducible QC and CI/Airflow usage.

Typical usage
-------------
python validate_schema.py --input data/call_level_table.csv --schema schemas/call_level.yaml
python validate_schema.py --input data/mouse_summary.parquet --schema schemas/mouse_summary.yaml

Schema format (YAML)
--------------------
version: 1
table_name: call_level_table
rules:                                       # optional table-level rules
  - name: duration_nonnegative
    expr: "Duration >= 0"
columns:
  Start_time:
    dtype: float
    required: true
    nullable: false
    min: 0
  End_time:
    dtype: float
    required: true
    nullable: false
    min: 0
  Duration:
    dtype: float
    required: true
    nullable: false
    min: 0
  Class:
    dtype: string
    required: true
    nullable: true
    allowed: ["Complex", "Simple", "Upward", "Downward"]   # example
"""

from __future__ import annotations

import argparse
import sys
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

try:
    import yaml  # pyyaml
except ImportError:  # pragma: no cover
    yaml = None


# ----------------------------
# Utilities / error structures
# ----------------------------

@dataclass
class ValidationIssue:
    level: str              # "ERROR" | "WARN"
    code: str               # machine-friendly code
    message: str            # human-friendly detail
    column: Optional[str] = None
    n_rows: Optional[int] = None
    examples: Optional[List[Any]] = None


def _load_yaml(path: str) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("pyyaml is required to load YAML schemas. Install: pip install pyyaml")
    with open(path, "r", encoding="utf-8") as f:
        obj = yaml.safe_load(f)
    if not isinstance(obj, dict):
        raise ValueError("Schema YAML must be a mapping/dict at top-level.")
    return obj


def _read_table(path: str) -> pd.DataFrame:
    p = path.lower()
    if p.endswith(".csv"):
        return pd.read_csv(path)
    if p.endswith(".parquet"):
        return pd.read_parquet(path)
    if p.endswith(".xlsx") or p.endswith(".xls"):
        # first sheet by default
        return pd.read_excel(path)
    raise ValueError(f"Unsupported input format: {path} (use .csv, .parquet, .xlsx)")


def _normalize_dtype_name(dtype: Any) -> str:
    """
    Convert pandas dtype to a simple comparable string.
    """
    s = str(dtype)
    # Normalize common pandas dtype strings
    if s.startswith("int"):
        return "int"
    if s.startswith("float"):
        return "float"
    if s in ("object", "string"):
        return "string"
    if s.startswith("datetime"):
        return "datetime"
    if s == "bool":
        return "bool"
    return s


def _coerce_string_series(s: pd.Series) -> pd.Series:
    # Keep NaN as NaN; cast non-nulls to str
    return s.where(s.isna(), s.astype(str))


def _safe_eval_expr(df: pd.DataFrame, expr: str) -> pd.Series:
    """
    Evaluate a boolean expression safely using pandas.eval with python engine.
    Expression example: "End_time >= Start_time"
    Returns boolean series, True where rule passes.
    """
    try:
        out = df.eval(expr, engine="python")
        if not isinstance(out, pd.Series):
            raise ValueError("Expression did not evaluate to a row-wise Series.")
        if out.dtype != bool:
            out = out.astype(bool)
        return out
    except Exception as e:
        raise ValueError(f"Failed to evaluate rule expr='{expr}': {e}") from e


# ----------------------------
# Core validation
# ----------------------------

def validate(df: pd.DataFrame, schema: Dict[str, Any]) -> Tuple[bool, List[ValidationIssue]]:
    issues: List[ValidationIssue] = []

    columns_spec: Dict[str, Any] = schema.get("columns", {}) or {}
    if not isinstance(columns_spec, dict) or len(columns_spec) == 0:
        issues.append(ValidationIssue(
            level="ERROR",
            code="SCHEMA_NO_COLUMNS",
            message="Schema must define a non-empty 'columns' mapping."
        ))
        return False, issues

    # 1) Required columns present
    required_cols = [c for c, spec in columns_spec.items() if (spec or {}).get("required", False)]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        issues.append(ValidationIssue(
            level="ERROR",
            code="MISSING_REQUIRED_COLUMNS",
            message=f"Missing required columns: {missing}",
            n_rows=len(missing),
            examples=missing
        ))

    # 2) Unexpected columns (warn only)
    allow_extra = bool(schema.get("allow_extra_columns", True))
    if not allow_extra:
        unexpected = [c for c in df.columns if c not in columns_spec]
        if unexpected:
            issues.append(ValidationIssue(
                level="WARN",
                code="UNEXPECTED_COLUMNS",
                message=f"Unexpected columns found (schema disallows extras): {unexpected}",
                n_rows=len(unexpected),
                examples=unexpected
            ))

    # 3) Column-level checks
    for col, spec in columns_spec.items():
        spec = spec or {}
        if col not in df.columns:
            continue  # already reported if required; skip deeper checks

        s = df[col]
        dtype_expected = spec.get("dtype", None)
        nullable = bool(spec.get("nullable", True))

        # 3a) Nullability
        if not nullable:
            n_null = int(s.isna().sum())
            if n_null > 0:
                examples = df.loc[s.isna(), col].head(5).tolist()
                issues.append(ValidationIssue(
                    level="ERROR",
                    code="NULLS_NOT_ALLOWED",
                    message=f"Column '{col}' contains {n_null} nulls but nullable=false.",
                    column=col,
                    n_rows=n_null,
                    examples=examples
                ))

        # 3b) Type checks (best-effort; we validate "compatible" rather than exact pandas dtype)
        if dtype_expected:
            dtype_expected = str(dtype_expected).lower().strip()
            actual_norm = _normalize_dtype_name(s.dtype)

            # If expected is string, tolerate object/string
            if dtype_expected == "string":
                if actual_norm not in ("string", "object"):
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="DTYPE_MISMATCH",
                        message=f"Column '{col}' expected dtype=string but got {s.dtype}.",
                        column=col
                    ))
            elif dtype_expected in ("int", "integer"):
                # allow int columns; warn if float with all .0 values could be int-like
                if actual_norm != "int":
                    # allow float if it is int-like
                    if actual_norm == "float" and s.dropna().apply(float.is_integer).all():
                        issues.append(ValidationIssue(
                            level="WARN",
                            code="DTYPE_INTLIKE_FLOAT",
                            message=f"Column '{col}' is float but appears int-like; consider casting to int.",
                            column=col
                        ))
                    else:
                        issues.append(ValidationIssue(
                            level="ERROR",
                            code="DTYPE_MISMATCH",
                            message=f"Column '{col}' expected dtype=int but got {s.dtype}.",
                            column=col
                        ))
            elif dtype_expected == "float":
                if actual_norm not in ("float", "int"):  # int is acceptable for float
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="DTYPE_MISMATCH",
                        message=f"Column '{col}' expected dtype=float but got {s.dtype}.",
                        column=col
                    ))
            elif dtype_expected == "bool":
                if actual_norm != "bool":
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="DTYPE_MISMATCH",
                        message=f"Column '{col}' expected dtype=bool but got {s.dtype}.",
                        column=col
                    ))
            elif dtype_expected == "datetime":
                if actual_norm != "datetime":
                    # Try coercion check without mutating df
                    coerced = pd.to_datetime(s, errors="coerce")
                    if coerced.isna().sum() != s.isna().sum():  # coercion introduced additional NaT
                        issues.append(ValidationIssue(
                            level="ERROR",
                            code="DTYPE_MISMATCH",
                            message=f"Column '{col}' expected datetime; coercion failed for some values.",
                            column=col
                        ))

        # 3c) Range checks (min/max)
        if "min" in spec or "max" in spec:
            # Attempt numeric conversion for range checks
            num = pd.to_numeric(s, errors="coerce")
            # ignore nulls
            valid = num.dropna()
            if "min" in spec:
                mn = float(spec["min"])
                bad = valid[valid < mn]
                if len(bad) > 0:
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="MIN_VIOLATION",
                        message=f"Column '{col}' has {len(bad)} values < min({mn}).",
                        column=col,
                        n_rows=int(len(bad)),
                        examples=bad.head(5).tolist()
                    ))
            if "max" in spec:
                mx = float(spec["max"])
                bad = valid[valid > mx]
                if len(bad) > 0:
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="MAX_VIOLATION",
                        message=f"Column '{col}' has {len(bad)} values > max({mx}).",
                        column=col,
                        n_rows=int(len(bad)),
                        examples=bad.head(5).tolist()
                    ))

        # 3d) Allowed set checks
        allowed = spec.get("allowed", None)
        if allowed is not None:
            allowed_set = set(allowed)
            ss = _coerce_string_series(s) if spec.get("dtype", "").lower() == "string" else s
            bad_mask = (~ss.isna()) & (~ss.isin(list(allowed_set)))
            n_bad = int(bad_mask.sum())
            if n_bad > 0:
                examples = df.loc[bad_mask, col].head(5).tolist()
                issues.append(ValidationIssue(
                    level="ERROR",
                    code="ALLOWED_SET_VIOLATION",
                    message=f"Column '{col}' has {n_bad} values not in allowed set.",
                    column=col,
                    n_rows=n_bad,
                    examples=examples
                ))

        # 3e) Regex checks (string columns)
        pattern = spec.get("regex", None)
        if pattern:
            ss = _coerce_string_series(s)
            bad_mask = (~ss.isna()) & (~ss.str.match(pattern))
            n_bad = int(bad_mask.sum())
            if n_bad > 0:
                examples = df.loc[bad_mask, col].head(5).tolist()
                issues.append(ValidationIssue(
                    level="ERROR",
                    code="REGEX_VIOLATION",
                    message=f"Column '{col}' has {n_bad} values not matching regex: {pattern}",
                    column=col,
                    n_rows=n_bad,
                    examples=examples
                ))

        # 3f) Uniqueness checks
        if bool(spec.get("unique", False)):
            dup_mask = s.duplicated(keep=False) & (~s.isna())
            n_dup = int(dup_mask.sum())
            if n_dup > 0:
                examples = df.loc[dup_mask, col].head(5).tolist()
                issues.append(ValidationIssue(
                    level="ERROR",
                    code="UNIQUE_VIOLATION",
                    message=f"Column '{col}' has {n_dup} duplicated entries but unique=true.",
                    column=col,
                    n_rows=n_dup,
                    examples=examples
                ))

    # 4) Primary key uniqueness (if provided)
    pk = schema.get("primary_key", None)
    if pk:
        if not isinstance(pk, list) or not all(isinstance(x, str) for x in pk):
            issues.append(ValidationIssue(
                level="ERROR",
                code="SCHEMA_PRIMARY_KEY_INVALID",
                message="Schema 'primary_key' must be a list of column names."
            ))
        else:
            missing_pk = [c for c in pk if c not in df.columns]
            if missing_pk:
                issues.append(ValidationIssue(
                    level="ERROR",
                    code="PRIMARY_KEY_MISSING_COLUMNS",
                    message=f"Primary key columns missing from table: {missing_pk}",
                    examples=missing_pk
                ))
            else:
                dup_rows = df.duplicated(subset=pk, keep=False)
                n_dup = int(dup_rows.sum())
                if n_dup > 0:
                    examples = df.loc[dup_rows, pk].head(5).to_dict(orient="records")
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="PRIMARY_KEY_NOT_UNIQUE",
                        message=f"Primary key {pk} is not unique; {n_dup} rows are duplicates.",
                        n_rows=n_dup,
                        examples=examples
                    ))

    # 5) Table-level boolean rules (expr)
    rules = schema.get("rules", []) or []
    if rules:
        if not isinstance(rules, list):
            issues.append(ValidationIssue(
                level="ERROR",
                code="SCHEMA_RULES_INVALID",
                message="Schema 'rules' must be a list."
            ))
        else:
            for r in rules:
                if not isinstance(r, dict):
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="SCHEMA_RULE_INVALID",
                        message=f"Rule must be dict, got: {type(r)}"
                    ))
                    continue
                name = r.get("name", "unnamed_rule")
                expr = r.get("expr", None)
                if not expr or not isinstance(expr, str):
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="SCHEMA_RULE_MISSING_EXPR",
                        message=f"Rule '{name}' missing 'expr' string."
                    ))
                    continue
                try:
                    ok = _safe_eval_expr(df, expr)
                    bad_mask = ~ok.fillna(False)
                    n_bad = int(bad_mask.sum())
                    if n_bad > 0:
                        examples = df.loc[bad_mask].head(3).to_dict(orient="records")
                        issues.append(ValidationIssue(
                            level="ERROR",
                            code="TABLE_RULE_VIOLATION",
                            message=f"Rule '{name}' failed for {n_bad} rows. expr={expr}",
                            n_rows=n_bad,
                            examples=examples
                        ))
                except Exception as e:
                    issues.append(ValidationIssue(
                        level="ERROR",
                        code="TABLE_RULE_EVAL_ERROR",
                        message=str(e)
                    ))

    is_valid = not any(i.level == "ERROR" for i in issues)
    return is_valid, issues


def _print_report(is_valid: bool, issues: List[ValidationIssue]) -> None:
    status = "VALID" if is_valid else "INVALID"
    print(f"\nSchema validation result: {status}")
    if not issues:
        print("No issues found.")
        return

    # Group by level
    errors = [i for i in issues if i.level == "ERROR"]
    warns = [i for i in issues if i.level == "WARN"]

    if errors:
        print("\nERRORS:")
        for i in errors:
            loc = f" [col={i.column}]" if i.column else ""
            n = f" (n={i.n_rows})" if i.n_rows is not None else ""
            print(f" - {i.code}{loc}{n}: {i.message}")
            if i.examples:
                print(f"   examples: {i.examples}")

    if warns:
        print("\nWARNINGS:")
        for i in warns:
            loc = f" [col={i.column}]" if i.column else ""
            n = f" (n={i.n_rows})" if i.n_rows is not None else ""
            print(f" - {i.code}{loc}{n}: {i.message}")
            if i.examples:
                print(f"   examples: {i.examples}")

    print()  # final newline


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a table file against a YAML schema.")
    parser.add_argument("--input", required=True, help="Path to CSV/Parquet/XLSX table file.")
    parser.add_argument("--schema", required=True, help="Path to YAML schema file.")
    args = parser.parse_args()

    schema = _load_yaml(args.schema)
    df = _read_table(args.input)

    is_valid, issues = validate(df, schema)
    _print_report(is_valid, issues)

    return 0 if is_valid else 2


if __name__ == "__main__":
    raise SystemExit(main())

