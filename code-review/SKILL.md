---
name: python-code-review
description: Production-grade Python code review. Checks architecture, security, quality, testing, docs. Provides actionable fix plans with severity levels.
---

# Python Code Review Skill

## Process

1. **Gather context**: `git diff --name-only main` to identify scope
2. **Run automated checks**: See [tooling.md](references/tooling.md) (ruff, vulture, mypy)
3. **Apply checklists**: Review against each reference file
4. **Generate report**: Categorized issues with fix suggestions

## Reference Files

| Area | File | Key Checks |
|------|------|------------|
| Architecture | [architecture.md](references/architecture.md) | Layer violations, circular deps |
| Security | [security.md](references/security.md) | Injection, secrets, auth |
| Quality | [quality.md](references/quality.md) | Complexity, error handling |
| Testing | [testing.md](references/testing.md) | tmp_path, mocking, assertions |
| Documentation | [documentation.md](references/documentation.md) | Docstrings, README accuracy |
| Deployment | [deployment.md](references/deployment.md) | Dockerfile, Helm, migrations |
| Consistency | [consistency.md](references/consistency.md) | Code-docs sync |
| Tooling | [tooling.md](references/tooling.md) | Ruff, vulture, mypy commands |

## Severity Calibration

| Level | Meaning | Examples |
|-------|---------|----------|
| 🔴 Critical | Blocks merge | SQL injection, hardcoded secrets, data loss |
| 🟠 High | Fix before merge | Layer violations, `/tmp` in tests, resource leaks |
| 🟡 Moderate | Should address | Missing tests, complexity >10, swallowed exceptions |
| 🔵 Low | Optional | Style beyond linter, minor refactoring |

## Output Format

```markdown
# Code Review Report
**Status**: PASS | NEEDS_WORK | BLOCKED
**Issues**: 🔴 N | 🟠 N | 🟡 N | 🔵 N

## [Category]
- 🟠 [HIGH] file:line - Issue description
  - 💡 Specific fix suggestion

## Fix Plan
### Plan 1: [Title]
- [ ] Action item
```

## Key Principles

1. **Be specific**: `"Add try/except at line 42 for ConnectionError"` not `"improve error handling"`
2. **Verify first**: Search/grep before suggesting existing functions exist
3. **Focus on diff**: Don't refactor untouched code
4. **No hallucinations**: Never reference functions without confirming they exist

## Project Config

If `code_review.yml` exists, apply its rules for custom layers, forbidden patterns, and thresholds.
