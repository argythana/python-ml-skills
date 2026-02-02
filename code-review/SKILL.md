---
name: python-code-review
description: Production-grade Python code review. Use when reviewing code, PRs, or analyzing code quality. Checks architecture, security, quality, testing, documentation, deployment, and consistency. Provides severity-rated issues with fix suggestions.
---

# Python Code Review

Systematic code review with actionable feedback organized by severity.

## Process

1. **Gather context**
   ```bash
   git diff --name-only main
   git diff main
   git log main..HEAD --oneline
   ```

2. **Run automated checks**
   ```bash
   ruff check --output-format=json <files>
   vulture --min-confidence=80 <files>
   mypy <files>
   ```

3. **Apply review checklists** - see references below

4. **Generate report** with issues and fix plan

## Severity Levels

| Level | Definition | Action |
|-------|------------|--------|
| Critical | Security flaws, data loss, breaking changes | Blocks merge |
| High | Resource leaks, wrong layer, N+1 queries | Fix before merge |
| Moderate | Missing tests, complexity >10, swallowed exceptions | Should address |
| Low | Style beyond linter, minor refactoring | Optional |

## Review Categories

Apply these checklists to changed files:

1. **Architecture** - Layer violations, dependency direction, god classes
   - See [references/architecture.md](references/architecture.md)

2. **Security** - Injection, secrets, path traversal, deserialization
   - See [references/security.md](references/security.md)

3. **Quality** - Complexity, error handling, performance
   - See [references/quality.md](references/quality.md)

4. **Testing** - Coverage, assertions, isolation, fixtures
   - See [references/testing.md](references/testing.md)

5. **Documentation** - Docstrings, README accuracy
   - See [references/documentation.md](references/documentation.md)

6. **Deployment** - Dockerfile, Helm, migrations
   - See [references/deployment.md](references/deployment.md)

7. **Consistency** - Code-docs sync, signature matches
   - See [references/consistency.md](references/consistency.md)

## Output Format

```markdown
# Code Review Report

**Status**: PASS | NEEDS_WORK | BLOCKED

## Issues
| Severity | Count |
|----------|-------|
| Critical | N |

### [Category]
- [severity] file:line - description
  - Fix: specific suggestion

## Fix Plan
1. [Issue] - [Action]
```

## Principles

- Be specific: "Add try/except at line 42" not "improve error handling"
- Verify first: Check functions exist before suggesting them
- Focus on changes: Don't refactor untouched code
- Provide working examples
