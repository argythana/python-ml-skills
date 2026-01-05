"""Markdown report generation utilities."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path


class MarkdownReport:
    """Builder for generating markdown reports."""

    def __init__(self, title: str):
        """Initialize a new report.

        Args:
            title: Report title.
        """
        self.title = title
        self.sections: list[str] = []
        self.metadata: dict[str, str] = {
            "generated_at": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"),
        }

    def add_metadata(self, key: str, value: str) -> MarkdownReport:
        """Add metadata to the report.

        Args:
            key: Metadata key.
            value: Metadata value.

        Returns:
            Self for chaining.
        """
        self.metadata[key] = value
        return self

    def add_section(self, heading: str, content: str, level: int = 2) -> MarkdownReport:
        """Add a section to the report.

        Args:
            heading: Section heading.
            content: Section content (markdown).
            level: Heading level (1-6).

        Returns:
            Self for chaining.
        """
        prefix = "#" * level
        self.sections.append(f"{prefix} {heading}\n\n{content}")
        return self

    def add_text(self, text: str) -> MarkdownReport:
        """Add raw text/markdown to the report.

        Args:
            text: Text to add.

        Returns:
            Self for chaining.
        """
        self.sections.append(text)
        return self

    def add_code_block(self, code: str, language: str = "") -> MarkdownReport:
        """Add a code block to the report.

        Args:
            code: Code content.
            language: Language for syntax highlighting.

        Returns:
            Self for chaining.
        """
        self.sections.append(f"```{language}\n{code}\n```")
        return self

    def add_table(
        self,
        headers: list[str],
        rows: list[list[str]],
        alignments: list[str] | None = None,
    ) -> MarkdownReport:
        """Add a markdown table to the report.

        Args:
            headers: Column headers.
            rows: Table rows (list of lists).
            alignments: Column alignments ('left', 'center', 'right').

        Returns:
            Self for chaining.
        """
        if alignments is None:
            alignments = ["left"] * len(headers)

        # Build header row
        header_row = "| " + " | ".join(headers) + " |"

        # Build separator row with alignments
        sep_parts = []
        for align in alignments:
            if align == "center":
                sep_parts.append(":---:")
            elif align == "right":
                sep_parts.append("---:")
            else:
                sep_parts.append("---")
        sep_row = "| " + " | ".join(sep_parts) + " |"

        # Build data rows
        data_rows = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]

        table = "\n".join([header_row, sep_row, *data_rows])
        self.sections.append(table)
        return self

    def add_summary_stats(self, stats: dict[str, str | int | float]) -> MarkdownReport:
        """Add a summary statistics block.

        Args:
            stats: Dictionary of statistic name to value.

        Returns:
            Self for chaining.
        """
        lines = []
        for key, value in stats.items():
            if isinstance(value, float):
                lines.append(f"- **{key}**: {value:,.4f}")
            elif isinstance(value, int):
                lines.append(f"- **{key}**: {value:,}")
            else:
                lines.append(f"- **{key}**: {value}")
        self.sections.append("\n".join(lines))
        return self

    def build(self) -> str:
        """Build the final markdown report.

        Returns:
            Complete markdown report as string.
        """
        parts = [f"# {self.title}\n"]

        # Add metadata block
        if self.metadata:
            meta_lines = [f"- **{k}**: {v}" for k, v in self.metadata.items()]
            parts.append("\n".join(meta_lines))
            parts.append("")

        # Add sections
        parts.extend(self.sections)

        return "\n\n".join(parts)

    def write(self, output: str | Path | None = None) -> None:
        """Write the report to file or stdout.

        Args:
            output: Output file path, or None for stdout.
        """
        content = self.build()

        if output is None:
            sys.stdout.write(content)
            sys.stdout.write("\n")
        else:
            Path(output).write_text(content)
