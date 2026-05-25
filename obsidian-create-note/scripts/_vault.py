"""Obsidian vault discovery for the obsidian-create-note skill.

Resolution order:
1. OBSIDIAN_VAULT env var, if set, must point to a directory containing .obsidian/.
2. Single directory under $HOME/Documents (searched up to depth 3) containing .obsidian/.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

MAX_DEPTH = 3


def _env_override() -> Path | None:
    value = os.environ.get("OBSIDIAN_VAULT")
    if not value:
        return None
    candidate = Path(value).expanduser()
    if not (candidate / ".obsidian").is_dir():
        print(
            f"OBSIDIAN_VAULT={value} does not point to an Obsidian vault "
            f"(missing {candidate}/.obsidian/).",
            file=sys.stderr,
        )
        sys.exit(1)
    return candidate


def _discover(root: Path, max_depth: int) -> list[Path]:
    found: list[Path] = []

    def walk(directory: Path, depth: int) -> None:
        if (directory / ".obsidian").is_dir():
            found.append(directory)
            return
        if depth >= max_depth:
            return
        try:
            entries = list(directory.iterdir())
        except OSError:
            return
        for entry in entries:
            if entry.is_dir() and not entry.name.startswith("."):
                walk(entry, depth + 1)

    walk(root, 0)
    return found


def find_vault() -> Path:
    override = _env_override()
    if override is not None:
        return override

    documents = Path.home() / "Documents"
    if not documents.is_dir():
        print(
            f"No Obsidian vault found: {documents} does not exist. "
            "Set OBSIDIAN_VAULT to the vault root.",
            file=sys.stderr,
        )
        sys.exit(1)

    candidates = _discover(documents, MAX_DEPTH)
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        print(
            f"No Obsidian vault found under {documents} (searched depth {MAX_DEPTH}). "
            "Set OBSIDIAN_VAULT to the vault root.",
            file=sys.stderr,
        )
        sys.exit(1)
    listing = "\n".join(f"  - {c}" for c in candidates)
    print(
        f"Multiple Obsidian vaults found under {documents}:\n{listing}\n"
        "Set OBSIDIAN_VAULT to pick one.",
        file=sys.stderr,
    )
    sys.exit(1)
