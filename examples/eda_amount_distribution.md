# Column Distribution: amount

- **generated_at**: 2026-01-05 08:57:54 UTC
- **source**: data/test_orders.parquet
- **column**: amount

## Summary

- **Total rows**: 10
- **Null/missing**: 1 (10.00%)
- **Non-null rows**: 9
- **Unique values**: 9
- **Cardinality**: Low

## Distribution

| Value | Count | Percentage | Cumulative |
| --- | ---: | ---: | ---: |
| 200.00 | 1 | 10.00% | 10.00% |
| 0.00 | 1 | 10.00% | 20.00% |
| 100.50 | 1 | 10.00% | 30.00% |
| 150.75 | 1 | 10.00% | 40.00% |
| 300.00 | 1 | 10.00% | 50.00% |
| 80.00 | 1 | 10.00% | 60.00% |
| 50.25 | 1 | 10.00% | 70.00% |
| 75.00 | 1 | 10.00% | 80.00% |
| 125.50 | 1 | 10.00% | 90.00% |

## Observations

- Low cardinality column (9 unique values) - suitable for categorical encoding
- Significant missing data (10.00%) - investigate missingness pattern
