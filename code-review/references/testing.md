# Testing Review

## High Priority Pitfalls (🟠)

### 1. Hardcoded Paths
```python
# ❌ recovery_dir = Path("/tmp/recovery")
# ✅ def test_x(tmp_path): recovery_dir = tmp_path / "recovery"
```
**Why:** Tests pass locally, fail in CI; leftover state causes "magic passes."

### 2. Blocking Calls
```python
# ❌ Tests hang because validate_brokers() blocks for 10s when Kafka unavailable
# ✅ @mock.patch("module._validate_brokers_reachable")
```

### 3. Config vs Data Mismatch
```python
# ❌ MIN_POSITIONS=5 but test sends 1 position → silently passes
# ✅ Either provide enough data OR: @mock.patch.dict(os.environ, {"MIN_POSITIONS": "1"})
```

### 4. Environment Variables
```python
# ❌ os.environ["KEY"] = "value"  # Leaks to other tests
# ✅ @mock.patch.dict(os.environ, {"KEY": "value"})
```

### 5. Mocking to Bypass Logic
```python
# ❌ @mock.patch("module.validate", return_value=True)  # Bypasses what you're testing!
# ✅ Test valid/invalid paths separately; only mock external dependencies
```

## Test Quality

| Issue | Severity | Fix |
|-------|----------|-----|
| No assertions | 🟠 High | Add `assert result.status == "expected"` |
| Flaky (time.sleep) | 🟠 High | Use explicit waits or async/await |
| Shared state | 🟡 Moderate | Create fixtures per test |
| Missing edge cases | 🟡 Moderate | Test empty, None, boundary values |

## Coverage Guidelines

| Code Type | Target |
|-----------|--------|
| Business logic | 90% |
| API endpoints | 80% |
| Utilities | 70% |

## Checklist

**High Priority:**
- [ ] Uses `tmp_path` for all file I/O
- [ ] Pre-flight checks mocked in logic tests
- [ ] Test data satisfies configured thresholds
- [ ] Environment mocked with `mock.patch.dict`
- [ ] Mocks don't bypass tested logic

**Standard:**
- [ ] New code has tests
- [ ] Meaningful assertions
- [ ] No flaky tests
