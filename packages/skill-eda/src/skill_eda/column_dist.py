#!/usr/bin/env python3
"""Column distribution analysis script.

Analyzes the value distribution of a specific column in a dataset
and produces a markdown report.

Usage:
    eda-column-dist --source <path> --column <name>
    eda-column-dist --source <path> --column <name> --output report.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ml_skills_core import (
    MarkdownReport,
    build_scan_query,
    get_connection,
    infer_source_type,
    quote_identifier,
    validate_identifier,
)


def assess_cardinality(unique_count: int, total_count: int) -> str:
    """Assess the cardinality level of a column."""
    if total_count == 0:
        return "Empty"
    ratio = unique_count / total_count
    if unique_count <= 10:
        return "Low"
    elif unique_count <= 100 or ratio < 0.01:
        return "Medium"
    elif ratio < 0.5:
        return "High"
    else:
        return "Very High (possibly unique identifier)"


def generate_observations(
    total: int,
    nulls: int,
    unique_count: int,
    top_value_pct: float,
) -> list[str]:
    """Generate automatic observations about the distribution."""
    observations = []

    # Cardinality observation
    cardinality = assess_cardinality(unique_count, total)
    if cardinality == "Low":
        observations.append(
            f"Low cardinality column ({unique_count} unique values) - suitable for categorical encoding"
        )
    elif cardinality == "Very High (possibly unique identifier)":
        observations.append(
            "Very high cardinality - may be an identifier column, consider excluding from features"
        )

    # Missing data observation
    null_pct = (nulls / total * 100) if total > 0 else 0
    if null_pct == 0:
        observations.append("No missing data")
    elif null_pct < 1:
        observations.append(f"Minimal missing data ({null_pct:.2f}%)")
    elif null_pct < 5:
        observations.append(f"Some missing data ({null_pct:.2f}%) - consider imputation strategy")
    else:
        observations.append(
            f"Significant missing data ({null_pct:.2f}%) - investigate missingness pattern"
        )

    # Imbalance observation
    if top_value_pct > 95:
        observations.append(
            f"Extreme imbalance: top value represents {top_value_pct:.1f}% of data"
        )
    elif top_value_pct > 80:
        observations.append(
            f"Class imbalance detected: top value represents {top_value_pct:.1f}% of data"
        )

    return observations


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze column value distribution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to data file",
    )
    parser.add_argument(
        "--column",
        required=True,
        help="Column name to analyze",
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Max unique values to display (default: 50)",
    )
    parser.add_argument(
        "--type",
        choices=["parquet", "csv", "json"],
        help="Override source type detection",
    )

    args = parser.parse_args()

    # Validate source exists
    source_path = Path(args.source)
    if not source_path.exists():
        sys.stderr.write(f"Error: Source not found: {args.source}\n")
        return 1

    # Validate column name
    if not validate_identifier(args.column):
        sys.stderr.write(f"Error: Invalid column name: {args.column}\n")
        return 1

    # Get connection and analyze
    conn = None
    try:
        conn = get_connection()
        source_type = args.type or infer_source_type(args.source)
        scan = build_scan_query(args.source, source_type)
        safe_col = quote_identifier(args.column)

        # Get total count
        result = conn.execute(f"SELECT COUNT(*) FROM {scan}").fetchone()
        if result is None:
            raise ValueError("Failed to get total count")
        total = result[0]

        # Get null count
        result = conn.execute(
            f"SELECT COUNT(*) FROM {scan} WHERE {safe_col} IS NULL"
        ).fetchone()
        if result is None:
            raise ValueError("Failed to get null count")
        nulls = result[0]

        # Get unique count
        result = conn.execute(
            f"SELECT COUNT(DISTINCT {safe_col}) FROM {scan}"
        ).fetchone()
        if result is None:
            raise ValueError("Failed to get unique count")
        unique_count = result[0]

        # Get value distribution
        distribution_query = f"""
            SELECT
                {safe_col} AS value,
                COUNT(*) AS count
            FROM {scan}
            WHERE {safe_col} IS NOT NULL
            GROUP BY {safe_col}
            ORDER BY count DESC
            LIMIT {args.limit}
        """
        distribution = conn.execute(distribution_query).fetchall()

    except Exception as e:
        sys.stderr.write(f"Error analyzing column: {e}\n")
        return 1
    finally:
        if conn is not None:
            conn.close()

    # Calculate percentages and cumulative
    non_null = total - nulls
    cumulative = 0
    dist_rows = []
    top_value_pct = 0

    for i, (value, count) in enumerate(distribution):
        pct = (count / total * 100) if total > 0 else 0
        cumulative += pct
        if i == 0:
            top_value_pct = pct

        # Format value for display
        display_value = str(value) if value is not None else "<NULL>"
        if len(display_value) > 50:
            display_value = display_value[:47] + "..."

        dist_rows.append([
            display_value,
            f"{count:,}",
            f"{pct:.2f}%",
            f"{cumulative:.2f}%",
        ])

    # Build report
    report = MarkdownReport(f"Column Distribution: {args.column}")
    report.add_metadata("source", args.source)
    report.add_metadata("column", args.column)

    # Summary section
    cardinality = assess_cardinality(unique_count, total)
    null_pct = (nulls / total * 100) if total > 0 else 0

    report.add_section("Summary", "")
    report.add_summary_stats({
        "Total rows": total,
        "Null/missing": f"{nulls:,} ({null_pct:.2f}%)",
        "Non-null rows": non_null,
        "Unique values": unique_count,
        "Cardinality": cardinality,
    })

    # Distribution table
    report.add_section("Distribution", "")
    if unique_count > args.limit:
        report.add_text(f"*Showing top {args.limit} of {unique_count} unique values*")
    report.add_table(
        headers=["Value", "Count", "Percentage", "Cumulative"],
        rows=dist_rows,
        alignments=["left", "right", "right", "right"],
    )

    # Observations
    observations = generate_observations(total, nulls, unique_count, top_value_pct)
    if observations:
        report.add_section("Observations", "")
        for obs in observations:
            report.add_text(f"- {obs}")

    # Write output
    report.write(args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
