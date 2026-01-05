---
name: eda
description: Exploratory Data Analysis for tabular data. Use this skill when analyzing value distributions, checking for missing data, computing correlations, examining class balance, or generating data quality reports.
---

# Exploratory Data Analysis (EDA)

Analyze tabular datasets to understand distributions, data quality, and relationships between variables.

## When to Use

- Understanding a new dataset before modeling
- Checking data quality (missing values, outliers, duplicates)
- Analyzing target variable distribution for classification/regression
- Identifying correlations between features
- Generating summary statistics

## Available Tasks

| Task | Script | Description |
|------|--------|-------------|
| Column Distribution | `column_dist.py` | Analyze value distribution for a specific column |

## Task Documentation

Detailed task templates are available in `tasks/`:
- `tasks/column_distribution.md` - Full documentation for column distribution analysis

## Quick Start

```bash
# Analyze distribution of a column
uv run python skills/eda/scripts/column_dist.py --source <path> --column <name>

# Save report to file
uv run python skills/eda/scripts/column_dist.py --source <path> --column <name> --output report.md
```

## Output Format

All EDA scripts produce markdown reports with:
- Task metadata (source, column, timestamp)
- Summary statistics
- Distribution tables or visualizations (as text)
- Observations and potential issues

## Best Practices

1. **Start with data-connector** - Verify data access and schema before EDA
2. **Check target variable first** - Understand class balance for classification tasks
3. **Look for missing patterns** - Missing data may not be random (MCAR/MAR/MNAR)
4. **Document findings** - Save reports for reproducibility

## Future Tasks (Planned)

- Missing data analysis
- Correlation matrix
- Outlier detection
- Duplicate detection
- Target class balance
- Full EDA report (combines all tasks)
