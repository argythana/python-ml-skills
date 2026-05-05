---
name: eda
description: >
  Use this skill when the user wants exploratory analysis of one tabular
  dataset (Parquet, CSV, JSON, JSONL) — column distributions, data quality,
  class balance, missing patterns, high-cardinality detection, or summary
  statistics. Trigger on prompts like "analyze this column", "check the
  distribution", "look for missing values", "is this target imbalanced", or
  "run EDA on this file". If the dataset path or column is missing, ask for
  it after routing. Do NOT use it just to verify a file is readable, list its
  schema, or count rows; use `dataset-inspector` first for basic access checks.
  Do NOT use it for model training, feature engineering, non-tabular data
  (images, text, audio), or remote warehouse exploration.
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
