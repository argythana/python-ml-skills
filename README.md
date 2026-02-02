# Python ML Skills

Claude Code skills for production-grade code review and exploratory data analysis.

## Installation

```bash
git clone https://github.com/argythana/python-ml-skills.git ~/.claude/skills/python-ml-skills
```

Add to your `~/.claude/CLAUDE.md`:

```markdown
import: ~/.claude/skills/python-ml-skills/code-review.md
import: ~/.claude/skills/python-ml-skills/eda.md
```

## Skills

| Skill | Description |
|-------|-------------|
| [code-review.md](code-review.md) | Python code review: architecture, security, quality, testing, docs |
| [eda.md](eda.md) | Exploratory data analysis for tabular datasets |

## Structure

```
python-ml-skills/
├── code-review.md      # Main skill (<100 lines)
├── eda.md              # Main skill (<100 lines)
├── references/         # Detailed content (loaded when needed)
│   ├── architecture.md
│   ├── security.md
│   ├── quality.md
│   ├── testing.md
│   ├── documentation.md
│   ├── deployment.md
│   ├── consistency.md
│   └── eda-analysis.md
└── README.md
```

## Usage

Ask Claude to review code or analyze data:

- "Review this PR for security issues"
- "Do a code review of the changes"
- "Analyze the distribution of the status column in data.parquet"
- "Check data quality for this dataset"

## Updating

```bash
cd ~/.claude/skills/python-ml-skills && git pull
```
