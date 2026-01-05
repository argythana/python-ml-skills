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
