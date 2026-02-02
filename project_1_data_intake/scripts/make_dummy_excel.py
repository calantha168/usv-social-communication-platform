import json
from pathlib import Path
import pandas as pd
import numpy as np

def schema_columns(schema: dict):
    # supports JSON Schema with "properties"
    props = schema.get("properties", {})
    return list(props.keys())

def default_value(prop_schema: dict, i: int):
    t = prop_schema.get("type")
    if isinstance(t, list):
        # pick first non-null type
        t = next((x for x in t if x != "null"), t[0])

    if t == "integer":
        return i
    if t == "number":
        return float(i) + 0.123
    if t == "boolean":
        return (i % 2 == 0)
    # string / fallback
    return f"example_{i}"

def main(schema_path: str, out_xlsx: str, n_rows: int = 25):
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    props = schema.get("properties", {})
    cols = schema_columns(schema)

    data = {}
    for c in cols:
        ps = props.get(c, {})
        data[c] = [default_value(ps, i) for i in range(n_rows)]

    df = pd.DataFrame(data)

    # helpful: if Start_time/End_time exist, make them consistent
    if "Start_time" in df.columns and "End_time" in df.columns:
        df["Start_time"] = np.arange(n_rows) * 0.1
        df["End_time"] = df["Start_time"] + 0.05

    Path(out_xlsx).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(out_xlsx, index=False)
    print(f"Wrote dummy Excel: {out_xlsx} with {len(df)} rows and {len(df.columns)} cols")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True, help="Path to JSON schema file")
    ap.add_argument("--out", required=True, help="Output .xlsx path")
    ap.add_argument("--rows", type=int, default=25)
    args = ap.parse_args()
    main(args.schema, args.out, args.rows)
