# Code Review Examples

Concrete examples of complete code reviews using this skill.

## Example 1: Simple PR Review

### Input
User: "Review this PR that adds a new user service"

**Changed files:**
- `src/services/user_service.py` (new)
- `tests/test_user_service.py` (new)

### Review Process

1. **Read the changed files**
2. **Run automated checks**: `ruff check src/services/user_service.py`
3. **Apply checklist** from each reference
4. **Generate report**

### Output

```markdown
# Code Review Report

**Status**: NEEDS_WORK ⚠️
**Files Reviewed**: 2
**Total Issues**: 4

## Issue Summary

| Severity | Count |
|----------|-------|
| 🔴 Critical | 1 |
| 🟠 High | 1 |
| 🟡 Moderate | 1 |
| 🔵 Low | 1 |

## Issues by Category

### Security
- 🔴 [CRITICAL] src/services/user_service.py:23 - SQL injection vulnerability
  - Query uses f-string: `f"SELECT * FROM users WHERE id = {user_id}"`
  - 💡 Use parameterized query: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`

### Code Quality
- 🟠 [HIGH] src/services/user_service.py:45 - Bare except clause
  - `except:` catches all exceptions including SystemExit
  - 💡 Use specific exception: `except ValueError:`

### Testing
- 🟡 [MODERATE] tests/test_user_service.py:12 - Test missing assertion
  - `test_create_user` calls function but doesn't assert result
  - 💡 Add: `assert result.id is not None`

### Documentation
- 🔵 [LOW] src/services/user_service.py:10 - Missing docstring
  - Public function `get_user()` has no documentation
  - 💡 Add docstring explaining purpose, args, and return

## Fix Plan

### Plan 1: Fix Security Vulnerability
*Effort: 10min*

**Issues addressed:**
- SQL injection in get_user()

**Actions:**
- [ ] Replace line 23 with parameterized query
- [ ] Add input validation for user_id
- [ ] Add test for SQL injection attempt

### Plan 2: Improve Code Quality
*Effort: 15min*

**Issues addressed:**
- Bare except clause
- Missing docstring

**Actions:**
- [ ] Replace `except:` with `except ValueError:`
- [ ] Add docstring to get_user()
- [ ] Add assertion to test_create_user
```

---

## Example 2: Architecture Violation

### Input
User: "Review changes to the utils package"

**Changed file:** `packages/utils/helpers.py`

```python
# packages/utils/helpers.py
import os
from sqlalchemy import create_engine

def get_user_discount(user_id: int) -> float:
    """Calculate discount for user."""
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.connect() as conn:
        result = conn.execute(f"SELECT total FROM orders WHERE user_id = {user_id}")
        total = result.scalar() or 0
    return min(total * 0.01, 0.2)  # Max 20% discount
```

### Review Output

```markdown
# Code Review Report

**Status**: BLOCKED 🚫
**Files Reviewed**: 1
**Total Issues**: 3

## Issues by Category

### Architecture
- 🔴 [CRITICAL] packages/utils/helpers.py:6 - Database access in utility layer
  - Utils package should contain pure functions without side effects
  - This function directly queries the database, violating layer separation
  - 💡 Move to `packages/data-access/user_repository.py` or refactor to accept data as parameter:
    ```python
    def calculate_discount(order_total: float) -> float:
        """Calculate discount based on order total."""
        return min(order_total * 0.01, 0.2)
    ```

### Security
- 🔴 [CRITICAL] packages/utils/helpers.py:8 - SQL injection vulnerability
  - User ID directly interpolated into query
  - 💡 Use parameterized query

### Code Quality
- 🟠 [HIGH] packages/utils/helpers.py:4 - Environment variable access
  - Utils should not access environment variables
  - 💡 Accept connection/engine as parameter

## Fix Plan

### Plan 1: Fix Architecture Violation
*Effort: 30min*

**Issues addressed:**
- Database access in utility layer
- Environment variable access
- SQL injection

**Actions:**
- [ ] Create `packages/data-access/order_repository.py`
- [ ] Move database query to `OrderRepository.get_total_for_user()`
- [ ] Refactor `helpers.py` to pure function accepting order total
- [ ] Update callers to fetch data first, then call utility
```

---

## Example 3: Missing Tests and Docs

### Input
User: "Quick review of the new feature"

**Changed files:**
- `src/features/export.py` (new, 150 lines)
- No test file

### Review Output

```markdown
# Code Review Report

**Status**: NEEDS_WORK ⚠️
**Files Reviewed**: 1
**Total Issues**: 3

## Issues by Category

### Testing
- 🟠 [HIGH] src/features/export.py - No tests for new module
  - 150 lines of new code without test coverage
  - Critical functions: `export_to_csv()`, `export_to_json()`, `validate_export_config()`
  - 💡 Create `tests/features/test_export.py` with:
    - `test_export_to_csv_with_valid_data`
    - `test_export_to_csv_with_empty_data`
    - `test_export_to_json_handles_nested_objects`
    - `test_validate_export_config_rejects_invalid`

### Documentation
- 🟡 [MODERATE] src/features/export.py - Missing module docstring
  - New module needs overview documentation
  - 💡 Add module docstring explaining purpose and usage

- 🔵 [LOW] src/features/export.py:45 - Missing function docstrings
  - `export_to_csv()` and `export_to_json()` lack documentation
  - 💡 Add Google-style docstrings with Args, Returns, Raises

## Deployment Gaps

⚠️ New feature may need:
- [ ] Documentation in user guide
- [ ] Entry in CHANGELOG
- [ ] Feature flag for gradual rollout
```

---

## Example 4: Clean PR (Pass)

### Input
User: "Review this refactoring PR"

### Review Output

```markdown
# Code Review Report

**Status**: PASS ✅
**Files Reviewed**: 5
**Total Issues**: 0

## Summary

This PR makes solid improvements:

✅ **Architecture**: Clean separation maintained
✅ **Security**: No new vulnerabilities
✅ **Code Quality**: Ruff passes, no dead code
✅ **Testing**: All new code has tests, coverage maintained
✅ **Documentation**: Docstrings updated to match changes

### Observations (non-blocking)

- Nice use of dataclasses in `models.py` - cleaner than dict
- Consider adding `__slots__` to `UserDTO` for memory efficiency (optional)

**Recommendation**: Approve and merge
```
