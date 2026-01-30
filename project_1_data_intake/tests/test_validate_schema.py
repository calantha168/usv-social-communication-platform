import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SRC = BASE_DIR / "src" / "validate_schema.py"
SCHEMA = BASE_DIR / "schemas" / "call_level.yaml"
EXAMPLES = BASE_DIR / "examples"


def run_validator(input_csv):
    result = subprocess.run(
        [sys.executable, SRC, "--input", input_csv, "--schema", SCHEMA],
        capture_output=True,
        text=True,
    )
    return result


def test_valid_call_level_passes():
    """Valid call-level table should pass schema validation."""
    result = run_validator(EXAMPLES / "sample_call_level.csv")
    assert result.returncode == 0
    assert "VALID" in result.stdout


def test_missing_required_column_fails():
    """Missing required column should fail validation."""
    result = run_validator(EXAMPLES / "bad_missing_col.csv")
    assert result.returncode != 0
    assert "MISSING_REQUIRED_COLUMNS" in result.stdout or "INVALID" in result.stdout


def test_logical_rule_violation_fails():
    """Logical rule violations (e.g., End_time < Start_time) should fail."""
    result = run_validator(EXAMPLES / "bad_logic.csv")
    assert result.returncode != 0
    assert "RULE" in result.stdout or "INVALID" in result.stdout
