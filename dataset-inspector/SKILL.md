---
name: dataset-inspector
description: >
  Use this skill when the user wants to inspect one local tabular file
  (Parquet, CSV, JSON, JSONL) — verify the file is readable, list columns and
  types, count rows, report file size, or produce a compact schema/connection
  report. Trigger on prompts like "inspect this dataset", "check the schema",
  "how many rows are in this file", "verify data access", or "what columns are
  in this parquet". If the file path is missing, ask for it after routing. Do
  NOT use it for exploratory statistics, distributions, missing patterns, or
  class balance; use `eda` after access is confirmed. Do NOT use it for model
  training, database connections (Postgres, MySQL, SQLite), remote data
  sources (S3, HTTPS, Snowflake, BigQuery), or non-tabular data (images, text,
  audio).
---

# Dataset Inspector

Inspect a local tabular data source and return a Markdown schema report.

## Workflow

1. Confirm the user provided a local data file path.
2. Run `scripts/dataset-inspect --source <path>`.
3. Use `--type parquet|csv|json` only when extension-based detection is wrong.
4. Use `--output <report.md>` when the report should be saved.
5. Summarize the row count, column count, file size, and notable schema details.

## Command

```bash
scripts/dataset-inspect --source data/sample.parquet
scripts/dataset-inspect --source data/sample.csv --output reports/schema.md
```

## Requirements

The helper script is self-contained except for `duckdb`. If it is unavailable,
install it in the active project environment before running the script.
