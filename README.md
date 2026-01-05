# Python ML Skills

Reusable Machine Learning skills for AI agents, distributed via Model Context Protocol (MCP).

Inspired by [Sionic AI's approach to logging ML experiments as reusable agent skills](https://huggingface.co/blog/sionic-ai/claude-code-skills-training).

## Overview

This repository provides general, reusable skill templates that many projects can connect to via MCP. Each skill contains:

- `SKILL.md` - Instructions for the agent
- `tasks/*.md` - Task templates with usage patterns
- `scripts/*.py` - DuckDB-based CLI scripts

## Available Skills

| Skill | Description |
|-------|-------------|
| `data-connector` | Connect to and inspect data sources |
| `eda` | Exploratory Data Analysis for tabular data |

## Installation

### Claude Code (MCP)

```bash
/plugin marketplace add <your-org>/python-ml-skills
/plugin install all-skills@python-ml-skills
```

### Manual Setup

```bash
git clone https://github.com/<your-org>/python-ml-skills.git
cd python-ml-skills
uv sync
```

## Quick Start

### 1. Inspect a data source

```bash
uv run python skills/data-connector/scripts/connect.py --source data/sample.parquet
```

### 2. Analyze column distribution

```bash
uv run python skills/eda/scripts/column_dist.py --source data/sample.parquet --column status
```

## Project Structure

```text
python-ml-skills/
├── .claude-plugin/
│   └── plugin.json           # MCP plugin manifest
├── shared/                   # Shared Python utilities
│   ├── connection.py         # DuckDB connection handling
│   └── report.py             # Markdown report generation
├── skills/
│   ├── data-connector/       # Data connection skill
│   │   ├── SKILL.md
│   │   └── scripts/
│   └── eda/                  # EDA skill
│       ├── SKILL.md
│       ├── tasks/
│       └── scripts/
└── docs/
    └── drafts/               # Design documents
```

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              python-ml-skills (THIS REPO)                   │
│  General, reusable skill templates distributed via MCP      │
└──────────────────────────────┬──────────────────────────────┘
                               │ MCP Connection
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    USER'S PROJECT                           │
│  - data/           (their data files)                       │
│  - reports/        (generated task reports)                 │
│  - logs/           (project-specific success/failure log)   │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

All scripts support:

- **stdout** (default) - pipe or redirect as needed
- **`--output <file>`** - write directly to file

Reports are generated in Markdown format for readability and version control.

## Contributing

1. Follow existing skill structure (`SKILL.md` + `tasks/` + `scripts/`)
2. Use `shared/` utilities for DuckDB and report generation
3. Scripts must work with `uv run python`
4. Keep skills data-source agnostic (no hardcoded file types in SKILL.md)
