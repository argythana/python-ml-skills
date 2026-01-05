# Column Distribution Analysis

Analyze the value distribution of a specific column in a dataset.

## Task Overview

| Item | Details |
|------|---------|
| **Script** | `skills/eda/scripts/column_dist.py` |
| **Input** | Data source path, column name |
| **Output** | Markdown report with distribution statistics |

## Usage

```bash
# Basic usage (stdout)
uv run python skills/eda/scripts/column_dist.py --source <path> --column <column_name>

# Save to file
uv run python skills/eda/scripts/column_dist.py --source <path> --column <column_name> --output report.md

# Limit output rows (for high-cardinality columns)
uv run python skills/eda/scripts/column_dist.py --source <path> --column <column_name> --limit 20
```

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--source` | Yes | - | Path to data file |
| `--column` | Yes | - | Column name to analyze |
| `--output` | No | stdout | Output file path |
| `--limit` | No | 50 | Max unique values to display |
| `--type` | No | auto | Source type override |

## Output Report Contents

1. **Summary Statistics**
   - Total rows
   - Null/missing count and percentage
   - Unique value count
   - Cardinality assessment (low/medium/high)

2. **Value Distribution Table**
   - Value
   - Count
   - Percentage of total
   - Cumulative percentage

3. **Observations**
   - Automatically generated notes about the distribution

## Example Output

```markdown
# Column Distribution: status

- **source**: data/orders.parquet
- **column**: status
- **generated_at**: 2025-01-05 10:30:00 UTC

## Summary

- **Total rows**: 1,234,567
- **Null/missing**: 123 (0.01%)
- **Unique values**: 5
- **Cardinality**: Low

## Distribution

| Value | Count | Percentage | Cumulative |
|-------|-------|------------|------------|
| completed | 987,654 | 80.00% | 80.00% |
| pending | 123,456 | 10.00% | 90.00% |
| cancelled | 61,728 | 5.00% | 95.00% |
| refunded | 49,382 | 4.00% | 99.00% |
| processing | 12,347 | 1.00% | 100.00% |

## Observations

- Low cardinality column (5 unique values) - suitable for categorical encoding
- Minimal missing data (0.01%)
- Class imbalance detected: 'completed' represents 80% of data
```

## When to Use

- Understanding categorical variable distributions
- Checking target variable class balance
- Identifying rare categories
- Detecting data quality issues (unexpected values)

## Common Patterns

### Healthy Distribution
- Expected values present
- Reasonable class balance (or expected imbalance)
- Low null percentage

### Warning Signs
- High null percentage (>5%)
- Unexpected categories (typos, encoding issues)
- Extreme imbalance for target variables
- Single value dominates (>99%)
