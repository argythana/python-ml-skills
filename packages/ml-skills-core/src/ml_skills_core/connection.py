"""DuckDB connection utilities for data access."""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

import duckdb

if TYPE_CHECKING:
    from duckdb import DuckDBPyConnection


def get_connection(database: str | None = None) -> DuckDBPyConnection:
    """Create a DuckDB connection.

    Args:
        database: Path to database file, or None for in-memory database.

    Returns:
        DuckDB connection object.
    """
    return duckdb.connect(database or ":memory:")


def validate_identifier(name: str) -> bool:
    """Validate that a string is a safe SQL identifier.

    Args:
        name: The identifier to validate.

    Returns:
        True if valid, False otherwise.
    """
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name))


def quote_identifier(name: str) -> str:
    """Safely quote a SQL identifier.

    Args:
        name: The identifier to quote.

    Returns:
        Quoted identifier string.

    Raises:
        ValueError: If identifier contains invalid characters.
    """
    if not validate_identifier(name):
        raise ValueError(f"Invalid identifier: {name}")
    return f'"{name}"'


def escape_string(value: str) -> str:
    """Escape a string value for SQL.

    Args:
        value: The string to escape.

    Returns:
        Escaped string safe for SQL.
    """
    return value.replace("'", "''")


def infer_source_type(source: str) -> str:
    """Infer the data source type from path or connection string.

    Args:
        source: Path or connection string.

    Returns:
        Source type: 'parquet', 'csv', 'json', 'database', or 'unknown'.
    """
    source_lower = source.lower()
    if source_lower.endswith(".parquet"):
        return "parquet"
    elif source_lower.endswith(".csv"):
        return "csv"
    elif source_lower.endswith(".json") or source_lower.endswith(".jsonl"):
        return "json"
    elif source_lower.endswith(".db") or source_lower.endswith(".duckdb"):
        return "database"
    elif "://" in source:
        return "database"
    return "unknown"


def build_scan_query(source: str, source_type: str | None = None) -> str:
    """Build a DuckDB scan query for the given source.

    Args:
        source: Path to data file or connection string.
        source_type: Override auto-detected source type.

    Returns:
        SQL query string to scan the source.

    Raises:
        ValueError: If source type cannot be determined.
    """
    if source_type is None:
        source_type = infer_source_type(source)

    safe_source = escape_string(source)

    if source_type == "parquet":
        return f"parquet_scan('{safe_source}')"
    elif source_type == "csv":
        return f"read_csv_auto('{safe_source}')"
    elif source_type == "json":
        return f"read_json_auto('{safe_source}')"
    elif source_type == "database":
        raise ValueError("Database connections require explicit table specification")
    else:
        raise ValueError(f"Unknown source type for: {source}")


def query_to_df(
    conn: DuckDBPyConnection,
    query: str,
) -> list[tuple]:
    """Execute a query and return results as list of tuples.

    Args:
        conn: DuckDB connection.
        query: SQL query to execute.

    Returns:
        List of result tuples.
    """
    return conn.execute(query).fetchall()


def get_table_info(
    conn: DuckDBPyConnection,
    source: str,
    source_type: str | None = None,
) -> dict:
    """Get basic information about a data source.

    Args:
        conn: DuckDB connection.
        source: Path to data file.
        source_type: Override auto-detected source type.

    Returns:
        Dictionary with table info (row_count, columns, file_size).
    """
    scan = build_scan_query(source, source_type)

    # Get row count
    result = conn.execute(f"SELECT COUNT(*) FROM {scan}").fetchone()
    row_count = result[0] if result else 0

    # Get column info
    columns = conn.execute(f"DESCRIBE SELECT * FROM {scan}").fetchall()
    column_info = [{"name": col[0], "type": col[1]} for col in columns]

    # Get file size if it's a file
    file_size = None
    path = Path(source)
    if path.exists():
        file_size = path.stat().st_size

    return {
        "source": source,
        "row_count": row_count,
        "column_count": len(column_info),
        "columns": column_info,
        "file_size_bytes": file_size,
    }
