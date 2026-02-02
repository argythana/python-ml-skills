# Automated Tooling

Run these checks before manual review.

## Linting (Ruff)

```bash
ruff check --output-format=json <files>
```

Key rules: E/W (style), F (pyflakes), I (isort), B (bugbear), C (complexity), C4 (comprehensions), UP (pyupgrade), ARG (unused args), D103/D200 (docstrings).

## Dead Code (Vulture)

```bash
vulture --min-confidence=80 <files>
```

## Type Checking (Mypy)

```bash
mypy --ignore-missing-imports <files>
```

## Git Context

```bash
git diff --name-only main          # Changed files
git diff main                       # Full diff
git log main..HEAD --oneline        # Commit history
```
