# Python ML Skills

Reusable Machine Learning skills for AI agents, distributed via Model Context Protocol (MCP).

Inspired by [Sionic AI's approach to logging ML experiments as reusable agent skills](https://huggingface.co/blog/sionic-ai/claude-code-skills-training).

## Overview

This repository is a UV workspace containing self-contained skill packages. Each skill includes:

- `SKILL.md` - Instructions for the agent
- `tasks/*.md` - Task templates with usage patterns
- `src/` - Python package with CLI tools

## Available Skills

| Package | Command | Description |
|---------|---------|-------------|
| `skill-data-connector` | `data-connect` | Connect to and inspect data sources |
| `skill-eda` | `eda-column-dist` | Exploratory Data Analysis for tabular data |
| `skill-code-review` | *(markdown only)* | Production-grade Python code review |

## Installation

### Development Setup (UV Workspace)

```bash
git clone https://github.com/<your-org>/python-ml-skills.git
cd python-ml-skills
uv sync
```

### Install Individual Skills

```bash
# Install from git subdirectory
pip install "skill-eda @ git+https://github.com/<your-org>/python-ml-skills#subdirectory=packages/skill-eda"

# Or use UV sources in your project
# pyproject.toml:
# [tool.uv.sources]
# skill-eda = { git = "https://github.com/<your-org>/python-ml-skills", subdirectory = "packages/skill-eda" }
```

### Claude Code (MCP)

```bash
/plugin marketplace add <your-org>/python-ml-skills
/plugin install skill-eda@python-ml-skills
```

## Quick Start

```bash
# Inspect a data source
data-connect --source data/sample.parquet

# Analyze column distribution
eda-column-dist --source data/sample.parquet --column status

# Save report to file
eda-column-dist --source data/sample.parquet --column status --output report.md
```

## Project Structure

```text
python-ml-skills/
├── pyproject.toml                      # Workspace root
├── .claude-plugin/
│   └── plugin.json                     # MCP plugin manifest
├── packages/
│   ├── ml-skills-core/                 # Shared utilities (DuckDB, reports)
│   │   ├── pyproject.toml
│   │   └── src/ml_skills_core/
│   │       ├── connection.py
│   │       └── report.py
│   │
│   ├── skill-data-connector/           # Data connector skill
│   │   ├── pyproject.toml
│   │   ├── SKILL.md
│   │   └── src/skill_data_connector/
│   │       └── connect.py
│   │
│   └── skill-eda/                      # EDA skill
│       ├── pyproject.toml
│       ├── SKILL.md
│       ├── tasks/
│       │   └── column_distribution.md
│       └── src/skill_eda/
│           └── column_dist.py
└── docs/
    └── drafts/
```

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              python-ml-skills (THIS REPO)                   │
│                                                             │
│  UV Workspace with self-contained skill packages            │
│  Each skill: SKILL.md + tasks/ + src/ (CLI tools)           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               │ pip install / UV sources / MCP
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER'S PROJECT                           │
│                                                             │
│  Install skills as dependencies:                            │
│  - pip install skill-eda                                    │
│  - UV workspace source                                      │
│  - MCP plugin                                               │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

All CLI tools support:

- **stdout** (default) - pipe or redirect as needed
- **`--output <file>`** - write directly to file

Reports are generated in Markdown format for readability and version control.

## Adding a New Skill

1. Create `packages/skill-<name>/`
2. Add `pyproject.toml` with dependency on `ml-skills-core`
3. Add `SKILL.md` with agent instructions
4. Add `tasks/*.md` for detailed task documentation
5. Add `src/skill_<name>/` with Python code
6. Define CLI entry points in `[project.scripts]`

## Contributing

1. Each skill must be self-contained (SKILL.md + code in same package)
2. Use `ml-skills-core` for DuckDB connection and report generation
3. Define CLI entry points via `[project.scripts]`
4. Keep SKILL.md data-source agnostic
