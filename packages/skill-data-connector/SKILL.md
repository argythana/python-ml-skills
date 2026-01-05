---
name: data-connector
description: Connect to and inspect data sources. Use this skill when you need to verify data access, inspect table schemas, check row counts, or understand the structure of a dataset before performing analysis.
---

# Data Connector

Connect to data sources and retrieve basic information about datasets.

## When to Use

- Before starting any data analysis task
- To verify data is accessible and readable
- To inspect column names and types
- To check dataset size (rows, columns, file size)

## Available Scripts

### `data-connect` - Inspect Data Source

Connects to a data source and returns schema and summary information.

```bash
# Basic usage (outputs to stdout)
data-connect --source <path>

# Save to file
data-connect --source <path> --output report.md
```

**Arguments:**

- `--source` (required): Path to data file or connection string
- `--output`: Output file path (default: stdout)
- `--type`: Override source type detection (parquet, csv, json)

## Output Format

The script produces a markdown report with:

- Source path and type
- Row count and column count
- File size (if applicable)
- Column listing with data types

## Example Output

```markdown
# Data Connection Report

- **source**: data/sales.parquet
- **type**: parquet
- **row_count**: 1,234,567
- **column_count**: 15
- **file_size**: 45.2 MB

## Columns

| Column | Type |
|--------|------|
| id | INTEGER |
| date | DATE |
| amount | DOUBLE |
| category | VARCHAR |
```

## Supported Data Sources

The connector auto-detects source type from file extension:

- `.parquet` - Apache Parquet files
- `.csv` - CSV files (auto-detects delimiter)
- `.json`, `.jsonl` - JSON files
- `.db`, `.duckdb` - DuckDB database files
