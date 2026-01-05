# User Guide

How to use these skills in other projects with Claude Code.

## Option 1: UV Workspace Source (Recommended)

In your project's `pyproject.toml`:

```toml
[project]
dependencies = ["skill-eda", "skill-data-connector"]

[tool.uv.sources]
skill-eda = { git = "https://github.com/<your-org>/python-ml-skills", subdirectory = "packages/skill-eda" }
skill-data-connector = { git = "https://github.com/<your-org>/python-ml-skills", subdirectory = "packages/skill-data-connector" }
```

Then run `uv sync`. CLI commands are now available:

```bash
data-connect --source data/mydata.parquet
eda-column-dist --source data/mydata.parquet --column target
```

## Option 2: Local Path

If both projects are on the same machine:

```toml
[project]
dependencies = ["skill-eda", "skill-data-connector"]

[tool.uv.sources]
skill-eda = { path = "../python-ml-skills/packages/skill-eda" }
skill-data-connector = { path = "../python-ml-skills/packages/skill-data-connector" }
```

## Option 3: Claude Code Plugin

Add the skills repo as a plugin in your project directory:

```text
/plugin add /path/to/python-ml-skills
```

Or from GitHub:

```text
/plugin marketplace add <your-org>/python-ml-skills
```

## Option 4: CLAUDE.md Reference

In your project, create/edit `CLAUDE.md`:

```markdown
# Project Instructions
## Available Skills
- `data-connect --source <path>` - Inspect data sources
- `eda-column-dist --source <path> --column <name>` - Column distribution analysis
```

## Option 5: Global Skills (All Projects)

Make skills available in every project via Claude Code's global user scope.

```bash
# 1. Symlink skills to global directory
mkdir -p ~/.claude/skills
ln -s /path/to/python-ml-skills/packages/skill-data-connector ~/.claude/skills/
ln -s /path/to/python-ml-skills/packages/skill-eda ~/.claude/skills/

# 2. Install CLI tools globally (isolated)
pipx install /path/to/python-ml-skills/packages/skill-eda
pipx install /path/to/python-ml-skills/packages/skill-data-connector

# 3. Restart Claude Code to load the skills
```

## Quick Start

```bash
cd /path/to/your-project
# Add dependencies to pyproject.toml (Option 1 or 2)
uv sync
# Use the CLI tools
data-connect --source data/myfile.parquet
eda-column-dist --source data/myfile.parquet --column status --output reports/status_dist.md
```

## Get the updated skills

When using git dependencies, UV caches the resolved commit. To get updates, you have options:

### Option 1: Force Update with uv sync

#### Re-fetch all git dependencies

`uv sync --refresh`

#### Or refresh specific package

`uv sync --refresh-package skill-eda`

### Option 2: Pin to a Branch (Auto-Update)

```toml
[tool.uv.sources]
skill-eda = { git = "<https://github.com/argythana/python-ml-skills>", subdirectory = "packages/skill-eda", branch = "main" }
```

Then uv sync --refresh gets the latest from main.

### Option 3: Pin to a Tag (Stable Releases)

```toml
[tool.uv.sources]
skill-eda = { git = "<https://github.com/argythana/python-ml-skills>", subdirectory = "packages/skill-eda", tag = "v0.2.0" }
```

This requires uv sync when you update the tag in pyproject.toml.

### Option 4: Pin to Specific Commit (Reproducible)

```toml
[tool.uv.sources]
skill-eda = { git = "<https://github.com/argythana/python-ml-skills>", subdirectory = "packages/skill-eda", rev = "cfea6b4" }
```

Option 4 is the most reproducible, requires manual update.

---

#### Summary

| Scenario                | Command                             |
|-------------------------|-------------------------------------|
| Get latest (cached)     | uv sync (uses cached commit)        |
| Force refresh           | uv sync --refresh                   |
| Refresh one package     | uv sync --refresh-package skill-eda |
| Changed tag/rev in toml | uv sync                             |

Recommendation: If you're actively developing the skills, use branch = "main" and run uv sync --refresh when you want updates. For production, pin to tags.
