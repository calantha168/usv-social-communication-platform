PROJECT 1 — Data Intake + Schema Validation (Reproducible QC Layer)

Built a schema-driven validation system that enforces analysis-table integrity before any modeling:
required columns, dtypes, null policies, valid ranges, allowed categories, uniqueness/primary keys,
and row-wise logical constraints (e.g., End_time >= Start_time, Duration >= 0). This prevents silent
data corruption, reduces analyst time lost to debugging, and enables reliable downstream inference
(mixed-effects, nonparametric tests, dashboards) by ensuring call/session/mouse tables are clean,
consistent, and audit-ready. Designed to run locally, in CI, or as an Airflow gate.

# Validate a table
python src/validate_schema.py --input data/call_level_table.csv --schema schemas/call_level.yaml

# Use in a pipeline (fail-fast)
python src/validate_schema.py --input outputs/mouse_summary.parquet --schema schemas/mouse_summary.yaml
echo $?
