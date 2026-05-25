# Python ML Skills

Claude Code and Codex skills for Python code review, exploratory data
analysis, local data inspection, and verified literature reviews.

This repository follows the skillden-friendly `skillz` pattern: each skill is
a top-level directory with a `SKILL.md` entry point and any supporting
`references/` or `scripts/` colocated inside that same directory.

## Installation

With skillden, add each skill by path:

```bash
skillden add code-review --config local \
  --repo /path/to/python-ml-skills --path code-review --mode link
skillden add eda --config local \
  --repo /path/to/python-ml-skills --path eda --mode link
skillden add dataset-inspector --config local \
  --repo /path/to/python-ml-skills --path dataset-inspector --mode link
skillden add do-literature-review --config local \
  --repo /path/to/python-ml-skills --path do-literature-review --mode link
```

For a plain Claude install:

```bash
git clone https://github.com/argythana/python-ml-skills.git ~/.claude/skills/python-ml-skills
```

## Skills

| Skill | Description |
| --- | --- |
| [code-review](code-review/SKILL.md) | Python code review: architecture, security, quality, testing, docs |
| [eda](eda/SKILL.md) | Exploratory analysis for tabular datasets |
| [dataset-inspector](dataset-inspector/SKILL.md) | Inspect local Parquet, CSV, JSON, or JSONL files |
| [do-literature-review](do-literature-review/SKILL.md) | Verified literature reviews with citation audit trails |

## Structure

```text
python-ml-skills/
├── code-review/
│   ├── SKILL.md
│   └── references/
├── eda/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── dataset-inspector/
│   ├── SKILL.md
│   └── scripts/
├── do-literature-review/
│   ├── SKILL.md
│   ├── examples.md
│   └── references/
└── scripts/
    └── validate-skills-frontmatter
```

## Validation

```bash
scripts/validate-skills-frontmatter            # validate working tree
scripts/validate-skills-frontmatter --staged   # validate staged index
```

The validator enforces skillden-friendly frontmatter: exact `name` and
`description` keys, folded descriptions, `name` matching the skill
directory, and `description` under 1024 characters (Codex's hard
limit). Requires Ruby.

### Pre-commit hook

Install the committed git hook so every `git commit` validates staged
SKILL.md files:

```bash
scripts/install-hooks
```

This symlinks `scripts/git-hooks/pre-commit` into `.git/hooks/`. CI
also runs the validator on every push and PR
(`.github/workflows/validate-skills.yml`).
