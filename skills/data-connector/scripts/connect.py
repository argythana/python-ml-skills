#!/usr/bin/env python3
"""Data connection and inspection script.

Connects to a data source and produces a markdown report with schema
and summary information.

Usage:
    uv run python skills/data-connector/scripts/connect.py --source <path>
    uv run python skills/data-connector/scripts/connect.py --source <path> --output report.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add shared utilities to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.connection import get_connection, get_table_info, infer_source_type
from shared.report import MarkdownReport


def format_file_size(size_bytes: int | None) -> str:
    """Format file size in human-readable format."""
    if size_bytes is None:
        return "N/A"
    size = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Connect to data source and inspect schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to data file or connection string",
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: stdout)",
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

    # Get connection and table info
    conn = None
    try:
        conn = get_connection()
        source_type = args.type or infer_source_type(args.source)
        info = get_table_info(conn, args.source, source_type)
    except Exception as e:
        sys.stderr.write(f"Error connecting to source: {e}\n")
        return 1
    finally:
        if conn is not None:
            conn.close()

    # Build report
    report = MarkdownReport("Data Connection Report")
    report.add_metadata("source", args.source)
    report.add_metadata("type", source_type)
    report.add_metadata("row_count", f"{info['row_count']:,}")
    report.add_metadata("column_count", str(info["column_count"]))
    report.add_metadata("file_size", format_file_size(info["file_size_bytes"]))

    # Add columns table
    report.add_section(
        "Columns",
        "",
        level=2,
    )
    report.add_table(
        headers=["Column", "Type"],
        rows=[[col["name"], col["type"]] for col in info["columns"]],
    )

    # Write output
    report.write(args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
