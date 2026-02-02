# Code-Documentation Consistency

## Core Principle

When code changes, documentation must change. Inconsistency erodes trust.

**Before suggesting a function exists, verify with grep/search.**

## What to Cross-Reference

| Documentation | Verify Against |
|--------------|----------------|
| README imports | Actual module paths |
| README examples | Current function signatures |
| Docstring params | Function signature |
| Docstring return type | Actual return |
| Config docs | Env vars code actually reads |
| API docs | Implemented endpoints |

## Common Issues (🟠 High)

```python
# Renamed function - README still references old name
# ❌ from utils import process_data  # Was renamed to transform_data

# Changed parameter - docstring outdated
# ❌ def fetch(url, max_wait=30):  # Docstring says "timeout"

# Moved module - import path wrong
# ❌ from utils.helpers import validate  # Moved to core.validation
```

## Verification

```bash
# Check if documented function exists
grep -r "def validate_input" src/

# Check if env var is read
grep -r "os.environ.*CLAIMED_VAR" src/
```

## Checklist

- [ ] README imports resolve
- [ ] README examples use current signatures
- [ ] Docstrings match function parameters
- [ ] Config docs list all env vars code reads
- [ ] No references to renamed/moved functions
