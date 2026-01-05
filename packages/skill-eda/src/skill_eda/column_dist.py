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
    if unique_count <= 100 or ratio < 0.01:
        return "Medium"
    if ratio < 0.5:
        return "High"
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
        observations.append("Very high cardinality - may be an identifier column, consider excluding from features")

    # Missing data observation
    null_pct = (nulls / total * 100) if total > 0 else 0
    if null_pct == 0:
        observations.append("No missing data")
    elif null_pct < 1:
        observations.append(f"Minimal missing data ({null_pct:.2f}%)")
    elif null_pct < 5:
        observations.append(f"Some missing data ({null_pct:.2f}%) - consider imputation strategy")
    else:
        observations.append(f"Significant missing data ({null_pct:.2f}%) - investigate missingness pattern")

    # Imbalance observation
    if top_value_pct > 95:
        observations.append(f"Extreme imbalance: top value represents {top_value_pct:.1f}% of data")
    elif top_value_pct > 80:
        observations.append(f"Class imbalance detected: top value represents {top_value_pct:.1f}% of data")

    return observations


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
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
    return parser.parse_args()


def query_column_stats(args: argparse.Namespace) -> tuple[int, int, int, list]:
    """Query column statistics from the data source."""
    conn = get_connection()
    try:
        source_type = args.type or infer_source_type(args.source)
        scan = build_scan_query(args.source, source_type)
        safe_col = quote_identifier(args.column)

        # Get total count
        result = conn.execute(f"SELECT COUNT(*) FROM {scan}").fetchone()  # noqa: S608
        if result is None:
            raise ValueError("Failed to get total count")
        total = result[0]

        # Get null count
        result = conn.execute(
            f"SELECT COUNT(*) FROM {scan} WHERE {safe_col} IS NULL"  # noqa: S608
        ).fetchone()
        if result is None:
            raise ValueError("Failed to get null count")
        nulls = result[0]

        # Get unique count
        result = conn.execute(
            f"SELECT COUNT(DISTINCT {safe_col}) FROM {scan}"  # noqa: S608
        ).fetchone()
        if result is None:
            raise ValueError("Failed to get unique count")
        unique_count = result[0]

        # Get value distribution
        # safe_col is sanitized via quote_identifier(), scan via build_scan_query()
        distribution_query = f"""
            SELECT
                {safe_col} AS value,
                COUNT(*) AS count
            FROM {scan}
            WHERE {safe_col} IS NOT NULL
            GROUP BY {safe_col}
            ORDER BY count DESC
            LIMIT ?
        """  # noqa: S608 - safe_col and scan are sanitized identifiers
        distribution = conn.execute(distribution_query, (args.limit,)).fetchall()

        return total, nulls, unique_count, distribution
    finally:
        conn.close()


def build_distribution_rows(
    distribution: list, total: int
) -> tuple[list[list[str]], float]:
    """Build distribution table rows and calculate top value percentage."""
    cumulative = 0.0
    dist_rows = []
    top_value_pct = 0.0

    for i, (value, count) in enumerate(distribution):
        pct = (count / total * 100) if total > 0 else 0
        cumulative += pct
        if i == 0:
            top_value_pct = pct

        # Format value for display
        display_value = str(value) if value is not None else "<NULL>"
        if len(display_value) > 50:
            display_value = display_value[:47] + "..."

        dist_rows.append(
            [
                display_value,
                f"{count:,}",
                f"{pct:.2f}%",
                f"{cumulative:.2f}%",
            ]
        )

    return dist_rows, top_value_pct


def build_report(
    args: argparse.Namespace,
    total: int,
    nulls: int,
    unique_count: int,
    dist_rows: list[list[str]],
    top_value_pct: float,
) -> MarkdownReport:
    """Build the markdown report."""
    non_null = total - nulls
    cardinality = assess_cardinality(unique_count, total)
    null_pct = (nulls / total * 100) if total > 0 else 0

    report = MarkdownReport(f"Column Distribution: {args.column}")
    report.add_metadata("source", args.source)
    report.add_metadata("column", args.column)

    # Summary section
    report.add_section("Summary", "")
    report.add_summary_stats(
        {
            "Total rows": total,
            "Null/missing": f"{nulls:,} ({null_pct:.2f}%)",
            "Non-null rows": non_null,
            "Unique values": unique_count,
            "Cardinality": cardinality,
        }
    )

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

    return report


def validate_inputs(args: argparse.Namespace) -> str | None:
    """Validate command line inputs. Returns error message or None if valid."""
    source_path = Path(args.source)
    if not source_path.exists():
        return f"Error: Source not found: {args.source}"

    if not validate_identifier(args.column):
        return f"Error: Invalid column name: {args.column}"

    return None


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Validate inputs
    error = validate_inputs(args)
    if error:
        sys.stderr.write(f"{error}\n")
        return 1

    # Query column statistics
    try:
        total, nulls, unique_count, distribution = query_column_stats(args)
    except Exception as e:
        sys.stderr.write(f"Error analyzing column: {e}\n")
        return 1

    # Build distribution rows
    dist_rows, top_value_pct = build_distribution_rows(distribution, total)

    # Build and write report
    report = build_report(args, total, nulls, unique_count, dist_rows, top_value_pct)
    report.write(args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
