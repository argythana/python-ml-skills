---
name: eda
description: >
  Use this skill when the user needs exploratory analysis for tabular data:
  analyze column distributions, check data quality, examine class balance,
  detect missing patterns, identify high-cardinality columns, or generate
  summary statistics. Trigger on requests like "analyze this column", "check
  the distribution", "look for missing values", or "is this target
  imbalanced". Do NOT use it just to verify a file is readable or list its
  schema; use `data-connector` first for basic access checks.
---

# Exploratory Data Analysis

Analyze tabular datasets to understand distributions, data quality, and
patterns.

## When To Use

- Understanding a new dataset before modeling
- Checking data quality such as missing values, outliers, and duplicates
- Analyzing target variable distribution
- Identifying class imbalance
- Generating summary statistics

## Analysis Process

1. Connect to data and inspect schema.
2. Analyze the target variable first.
3. Check each relevant column for distribution, missingness, and cardinality.
4. Document findings in a compact report.

## Helper

For local Parquet, CSV, JSON, or JSONL files, use:

```bash
scripts/eda-column-dist --source data/sample.parquet --column status
```

The helper script requires `duckdb` in the active Python environment.

## Reference

For detailed analysis methodology and output format, read
[references/eda-analysis.md](references/eda-analysis.md).
