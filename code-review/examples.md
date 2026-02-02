# Code Review Examples

## Example 1: Security + Quality Issues

**Input:** "Review this PR adding a user service"

```markdown
# Code Review Report
**Status**: BLOCKED 🚫
**Issues**: 🔴 1 | 🟠 2 | 🟡 1

## Security
- 🔴 [CRITICAL] user_service.py:23 - SQL injection
  - `f"SELECT * FROM users WHERE id = {user_id}"`
  - 💡 Use parameterized query

## Quality
- 🟠 [HIGH] user_service.py:45 - Bare except clause
  - 💡 Use specific exception: `except ValueError:`

## Testing
- 🟠 [HIGH] test_user_service.py:12 - No assertion
  - 💡 Add: `assert result.id is not None`

## Documentation
- 🟡 [MODERATE] user_service.py:10 - Missing docstring
  - 💡 Add Google-style docstring
```

---

## Example 2: Architecture Violation

**Input:** "Review changes to utils package"

```python
# packages/utils/helpers.py - DB access in utility layer!
def get_user_discount(user_id: int) -> float:
    engine = create_engine(os.environ["DATABASE_URL"])
    result = conn.execute(f"SELECT total FROM orders WHERE user_id = {user_id}")
    return min(result.scalar() * 0.01, 0.2)
```

```markdown
# Code Review Report
**Status**: BLOCKED 🚫
**Issues**: 🔴 1 | 🟠 2

## Security
- 🔴 [CRITICAL] helpers.py:5 - SQL injection

## Architecture
- 🟠 [HIGH] helpers.py:3 - DB access in utility layer
  - 💡 Move to data-access; refactor to pure function:
    `def calculate_discount(total: float) -> float`

- 🟠 [HIGH] helpers.py:3 - Environment variable in utils
  - 💡 Accept engine as parameter
```

---

## Example 3: Test Pitfalls

**Input:** "Review the new test file"

```python
# tests/test_processor.py
def test_recovery():
    recovery_dir = Path("/tmp/recovery")  # ❌ Hardcoded!
    ...

def test_classifier():
    # MIN_POSITIONS=5 but only sending 1
    result = classify([single_position])
    assert result is None  # ❌ Passes for wrong reason!

@mock.patch("processor.validate", return_value=True)  # ❌ Bypasses logic!
def test_process(mock_validate):
    result = process(invalid_data)
```

```markdown
# Code Review Report
**Status**: NEEDS_WORK ⚠️
**Issues**: 🟠 4

## Testing
- 🟠 [HIGH] test_processor.py:3 - Hardcoded `/tmp` path
  - 💡 Use `tmp_path` fixture

- 🟠 [HIGH] test_processor.py:7 - Config/data mismatch
  - 💡 Provide enough data OR override threshold

- 🟠 [HIGH] test_processor.py:11 - Mock bypasses tested logic
  - 💡 Test validation separately

- 🟠 [HIGH] test_processor.py:8 - Weak assertion
  - 💡 Assert what SHOULD happen
```

---

## Example 4: Clean PR

```markdown
# Code Review Report
**Status**: PASS ✅
**Issues**: 🔴 0 | 🟠 0 | 🟡 0 | 🔵 0

## Summary
✅ Architecture: Clean separation
✅ Security: No vulnerabilities
✅ Testing: Uses tmp_path, data matches thresholds
✅ Documentation: Docstrings updated

**Recommendation:** Approve and merge
```
