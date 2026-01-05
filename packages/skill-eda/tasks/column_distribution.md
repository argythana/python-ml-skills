# Column Distribution Analysis

Analyze the value distribution of a specific column in a dataset.

## Task Overview

| Item | Details |
| ------ | --------- |
| **Command** | `eda-column-dist` |
| **Input** | Data source path, column name |
| **Output** | Markdown report with distribution statistics |

## Usage

```bash
# Basic usage (stdout)
eda-column-dist --source <path> --column <column_name>

# Save to file
eda-column-dist --source <path> --column <column_name> --output report.md

# Limit output rows (for high-cardinality columns)
eda-column-dist --source <path> --column <column_name> --limit 20
```

## Arguments

| Argument | Required | Default | Description |
| ---------- | ---------- | --------- | ------------- |
| `--source` | Yes | - | Path to data file |
| `--column` | Yes | - | Column name to analyze |
| `--output` | No | stdout | Output file path |
| `--limit` | No | 50 | Max unique values to display |
| `--type` | No | auto | Source type override |

## Output Report Contents

1. **Summary Statistics**
   - Total rows
   - Null/missing count and percentage
   - Non-null rows
   - Unique value count
   - Cardinality assessment (Empty/Low/Medium/High/Very High)

2. **Value Distribution Table**
   - Value (truncated to 50 characters if longer)
   - Count
   - Percentage of total
   - Cumulative percentage
   - Note: Shows top N values based on `--limit` parameter

3. **Observations**
   - Automatically generated notes based on:
     - Cardinality level and suitability for encoding
     - Missing data patterns (0%, <1%, 1-5%, >5%)
     - Class imbalance detection (>80%, >95%)
     - Possible identifier column detection

## Example Output

### Example: Low Cardinality Column

```markdown
# Column Distribution: status

- **source**: data/orders.parquet
- **column**: status
- **generated_at**: 2025-01-05 10:30:00 UTC

## Summary

- **Total rows**: 1,234,567
- **Null/missing**: 123 (0.01%)
- **Non-null rows**: 1,234,444
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
- Class imbalance detected: top value represents 80.0% of data
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
- Low null percentage (<1%)

### Cardinality Levels

- **Empty**: No data
- **Low**: ≤10 unique values - ideal for categorical encoding
- **Medium**: 11-100 unique values or <1% of total rows - may need encoding strategy
- **High**: >100 unique values and 1-50% of total rows - consider grouping or binning
- **Very High**: >50% of total rows - likely an identifier, exclude from features

### Observation Patterns

**Missing Data**:

- 0%: "No missing data"
- <1%: "Minimal missing data (X%)"
- 1-5%: "Some missing data (X%) - consider imputation strategy"
- >5%: "Significant missing data (X%) - investigate missingness pattern"

**Class Imbalance**:

- >80%: "Class imbalance detected: top value represents X% of data"
- >95%: "Extreme imbalance: top value represents X% of data"

### Warning Signs

- High null percentage (>5%)
- Unexpected categories (typos, encoding issues)
- Extreme imbalance for target variables
- Single value dominates (>99%)
