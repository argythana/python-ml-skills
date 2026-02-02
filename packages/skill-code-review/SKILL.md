---
name: python-code-review
description: Production-grade Python code review from a lead developer perspective. Use when reviewing Python code, PRs, or asking for code quality analysis. Checks architecture compliance, security, code quality (ruff, dead code), testing, documentation, and code-docs consistency. Provides actionable fix plans.
---

# Python Code Review Skill

Perform thorough code reviews as a production-grade lead Python developer. This skill provides systematic analysis across multiple dimensions with actionable feedback.

## Quick Start

When asked to review code or a PR:

1. **Gather context** - Identify changed files, understand the scope
2. **Run automated checks** - Linting, dead code, type checking
3. **Apply review checklist** - Architecture, security, quality, testing, docs
4. **Generate report** - Categorized issues with severity and fix suggestions

## Review Process

### Step 1: Understand the Change

Before reviewing, understand what you're looking at:

```bash
# Get list of changed files
git diff --name-only main

# See the actual changes
git diff main

# Check commit messages for context
git log main..HEAD --oneline
```

### Step 2: Run Automated Checks

Run these tools to catch mechanical issues:

**Linting with Ruff:**
```bash
ruff check --output-format=json <files>
```

**Dead Code Detection:**
```bash
vulture --min-confidence=80 <files>
```

**Type Checking (if project uses types):**
```bash
mypy <files>
```

### Step 3: Apply Review Checklist

For each changed file, systematically check:

1. **Architecture** - See [references/architecture.md](references/architecture.md)
2. **Security** - See [references/security.md](references/security.md)
3. **Code Quality** - See [references/quality.md](references/quality.md)
4. **Testing** - See [references/testing.md](references/testing.md)
5. **Documentation** - See [references/documentation.md](references/documentation.md)
6. **Deployment** - See [references/deployment.md](references/deployment.md)

### Step 4: Check Code-Documentation Consistency

Verify that:
- README examples match actual code
- Docstrings match function signatures
- API documentation reflects current implementation
- Configuration docs match actual config options

### Step 5: Generate Fix Plan

For each issue found:
1. Categorize by type (architecture, security, quality, etc.)
2. Assign severity (Critical, High, Moderate, Low)
3. Provide specific fix suggestion with code example
4. Estimate effort to fix

## Output Format

Structure your review as:

```markdown
# Code Review Report

**Status**: PASS | NEEDS_WORK | BLOCKED
**Files Reviewed**: N
**Total Issues**: N

## Issue Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | N |
| 🟠 High | N |
| 🟡 Moderate | N |
| 🔵 Low | N |

## Issues by Category

### Architecture
- [severity] file:line - description
  - 💡 Suggestion: ...

## Fix Plan

### Plan 1: [Title]
*Effort: 15min*

**Issues addressed:**
- Issue 1

**Actions:**
- [ ] Step 1
- [ ] Step 2
```

## Severity Guidelines

| Level | Emoji | Meaning | Examples |
|-------|-------|---------|----------|
| Critical | 🔴 | Blocks merge | Security vulnerabilities, architectural violations, data loss risks |
| High | 🟠 | Fix before merge | Runtime bugs, missing error handling, missing critical tests |
| Moderate | 🟡 | Should address | Code quality, missing tests, incomplete docs |
| Low | 🔵 | Nice to have | Style, minor docs, refactoring suggestions |

## Key Principles

### Be Specific, Not Vague
❌ "Improve error handling"
✅ "Add try/except around line 42 to handle ConnectionError"

### Verify Before Suggesting
❌ "Use the existing validate_input() function" (without checking it exists)
✅ "Use utils.validate_input() from src/utils/validation.py:23"

### Focus on Changed Code
- Don't suggest refactoring untouched legacy code
- Only flag issues in the diff unless they directly impact changes

### Provide Working Examples
```python
# Instead of vague: "add error handling"
# Provide specific:
try:
    result = api_client.fetch(endpoint)
except ConnectionError as e:
    logger.error(f"API connection failed: {e}")
    raise ServiceUnavailableError("External API unavailable") from e
```

## Common Patterns to Flag

See detailed patterns in reference files:
- [Architecture patterns](references/architecture.md)
- [Security patterns](references/security.md)
- [Quality patterns](references/quality.md)

## Project Configuration

If the project has a `code_review.yml`, load and apply those rules for:
- Custom architecture layers and constraints
- Project-specific forbidden patterns
- Required test coverage thresholds
- Documentation requirements
