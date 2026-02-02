# EDA Column Distribution Analysis

Detailed methodology for analyzing column distributions in tabular data.

## Analysis Steps

### 1. Connect to Data Source

Use DuckDB for fast, in-process SQL execution:

```python
import duckdb

conn = duckdb.connect(":memory:")

# For Parquet
df = conn.execute("SELECT * FROM parquet_scan('data.parquet')").fetchdf()

# For CSV
df = conn.execute("SELECT * FROM read_csv_auto('data.csv')").fetchdf()

# For JSON
df = conn.execute("SELECT * FROM read_json_auto('data.json')").fetchdf()
```

### 2. Compute Summary Statistics

```sql
-- Total count
SELECT COUNT(*) FROM source;

-- Null count
SELECT COUNT(*) FROM source WHERE column IS NULL;

-- Unique count
SELECT COUNT(DISTINCT column) FROM source;

-- Value distribution (top N)
SELECT
    column AS value,
    COUNT(*) AS count
FROM source
WHERE column IS NOT NULL
GROUP BY column
ORDER BY count DESC
LIMIT 50;
```

### 3. Assess Cardinality

```python
def assess_cardinality(unique_count: int, total_count: int) -> str:
    if total_count == 0:
        return "Empty"
    ratio = unique_count / total_count
    if unique_count <= 10:
        return "Low"
    if unique_count <= 100 or ratio < 0.01:
        return "Medium"
    if ratio < 0.5:
        return "High"
    return "Very High (possibly unique identifier)"
```

| Level | Criteria | Recommendation |
|-------|----------|----------------|
| Empty | No data | Investigate data source |
| Low | ≤10 unique values | Ideal for categorical encoding |
| Medium | 11-100 or <1% of rows | May need encoding strategy |
| High | >100 and <50% of rows | Consider grouping or binning |
| Very High | >50% of rows | Likely identifier, exclude from features |

### 4. Generate Observations

Auto-generate insights based on patterns:

**Cardinality Observation:**
```python
if cardinality == "Low":
    f"Low cardinality column ({unique_count} unique values) - suitable for categorical encoding"
elif cardinality == "Very High":
    "Very high cardinality - may be an identifier column, consider excluding from features"
```

**Missing Data Observation:**
```python
null_pct = nulls / total * 100
if null_pct == 0:
    "No missing data"
elif null_pct < 1:
    f"Minimal missing data ({null_pct:.2f}%)"
elif null_pct < 5:
    f"Some missing data ({null_pct:.2f}%) - consider imputation strategy"
else:
    f"Significant missing data ({null_pct:.2f}%) - investigate missingness pattern"
```

**Class Imbalance Observation:**
```python
top_value_pct = top_count / total * 100
if top_value_pct > 95:
    f"Extreme imbalance: top value represents {top_value_pct:.1f}% of data"
elif top_value_pct > 80:
    f"Class imbalance detected: top value represents {top_value_pct:.1f}% of data"
```

## Output Report Format

```markdown
# Column Distribution: {column_name}

- **source**: path/to/data.parquet
- **column**: column_name
- **generated_at**: 2025-01-05 10:30:00 UTC

## Summary

- **Total rows**: 1,234,567
- **Null/missing**: 123 (0.01%)
- **Non-null rows**: 1,234,444
- **Unique values**: 5
- **Cardinality**: Low

## Distribution

| Value | Count | Percentage | Cumulative |
|-------|------:|----------:|----------:|
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

## Warning Signs to Flag

| Pattern | Concern | Action |
|---------|---------|--------|
| High null % (>5%) | Data quality issue | Investigate source |
| Unexpected categories | Typos, encoding issues | Clean data |
| Extreme imbalance (>95%) | Model bias risk | Consider resampling |
| Single value (>99%) | No predictive value | Drop column |
| Very high cardinality | Identifier column | Exclude from features |

## Missingness Patterns

| Type | Definition | Detection |
|------|------------|-----------|
| MCAR | Missing Completely At Random | No pattern in missing values |
| MAR | Missing At Random | Depends on other observed variables |
| MNAR | Missing Not At Random | Depends on the missing value itself |

To investigate: check if nulls correlate with other columns.

## Best Practices

1. **Check target variable first** - Understand class balance before feature analysis
2. **Look for missing patterns** - Check if nulls are random or systematic
3. **Document all findings** - Save reports for reproducibility
4. **Compare train/test distributions** - Ensure consistency
