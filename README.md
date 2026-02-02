# Python ML Skills

Claude Code skills for production-grade code review and exploratory data analysis.

## Installation

```bash
git clone https://github.com/argythana/python-ml-skills.git ~/.claude/skills/python-ml-skills
```

Skills are auto-discovered from `~/.claude/skills/` - no CLAUDE.md imports needed.

## Skills

| Skill | Description |
|-------|-------------|
| [code-review](code-review/SKILL.md) | Python code review: architecture, security, quality, testing, docs |
| [eda](eda/SKILL.md) | Exploratory data analysis for tabular datasets |

## Structure

```text
python-ml-skills/
├── code-review/
│   ├── SKILL.md              # Main skill (<100 lines)
│   └── references/           # Detailed checklists
│       ├── architecture.md
│       ├── security.md
│       ├── quality.md
│       ├── testing.md
│       ├── documentation.md
│       ├── deployment.md
│       └── consistency.md
├── eda/
│   ├── SKILL.md              # Main skill (<100 lines)
│   └── references/
│       └── eda-analysis.md   # Analysis methodology
└── README.md
```

## Usage

Ask Claude to review code or analyze data:

- "Review this PR"
- "Do a code review focusing on security"
- "Analyze the distribution of the status column"
- "Check data quality for this dataset"

## Updating

```bash
cd ~/.claude/skills/python-ml-skills && git pull
```
