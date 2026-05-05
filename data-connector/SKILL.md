---
name: data-connector
description: >
  Use this skill when the user needs to inspect a local tabular data source
  before analysis: verify that a Parquet, CSV, JSON, or JSONL file is readable,
  list columns and types, count rows, or produce a compact data connection
  report. Trigger on requests like "inspect this dataset", "check the schema",
  "how many rows are in this file", or "verify data access". Do NOT use it for
  exploratory statistics, model training, database administration, remote data
  warehouse setup, or broad data-quality analysis; use `eda` for distributions
  and other analysis after basic access is confirmed.
---

# Data Connector

Inspect a local tabular data source and return a Markdown schema report.

## Workflow

1. Confirm the user provided a local data file path.
2. Run `scripts/data-connect --source <path>`.
3. Use `--type parquet|csv|json` only when extension-based detection is wrong.
4. Use `--output <report.md>` when the report should be saved.
5. Summarize the row count, column count, file size, and notable schema details.

## Command

```bash
scripts/data-connect --source data/sample.parquet
scripts/data-connect --source data/sample.csv --output reports/schema.md
```

## Requirements

The helper script is self-contained except for `duckdb`. If it is unavailable,
install it in the active project environment before running the script.
