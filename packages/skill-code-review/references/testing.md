# Testing Review Checklist

## Core Principle: Test What Matters

Good tests provide confidence that code works correctly without being brittle or slow.

## Test Coverage Requirements

### New Code Must Have Tests

**Flag when:**
- New functions/classes have no corresponding tests
- New features lack integration tests
- Bug fixes don't include regression tests

**Minimum expectations:**
- Unit tests for business logic
- Integration tests for data access
- End-to-end tests for critical user flows

### Coverage Thresholds

| Code Type | Minimum Coverage |
|-----------|------------------|
| Core business logic | 90% |
| API endpoints | 80% |
| Utilities | 70% |
| Scripts/CLI | 50% |

## Test Quality Checks

### Tests Must Have Assertions (🟠 High)

```python
# ❌ Test without meaningful assertions
def test_process_data():
    result = process_data(input_data)
    # No assertion - test always passes!

# ❌ Weak assertion
def test_process_data():
    result = process_data(input_data)
    assert result  # Only checks truthiness

# ✅ Meaningful assertions
def test_process_data():
    result = process_data(input_data)
    assert result.status == "success"
    assert result.count == 5
    assert "expected_key" in result.data
```

### Test Isolation (🟠 High)

**Flag tests that:**
- Depend on execution order
- Share mutable state
- Require external services without mocking
- Use real databases in unit tests

```python
# ❌ Tests share state
class TestUser:
    user = None  # Shared across tests!
    
    def test_create(self):
        self.user = User.create(name="test")
        
    def test_delete(self):
        self.user.delete()  # Depends on test_create running first!

# ✅ Each test is independent
class TestUser:
    def test_create(self):
        user = User.create(name="test")
        assert user.id is not None
        
    def test_delete(self):
        user = User.create(name="test")
        user.delete()
        assert User.find(user.id) is None
```

### Proper Mocking (🟡 Moderate)

**Flag:**
- Mocking internal implementation details
- Over-mocking (everything is mocked)
- Mock not matching real interface

```python
# ❌ Over-mocking - tests nothing real
def test_service(mocker):
    mocker.patch("service.validate")
    mocker.patch("service.process")
    mocker.patch("service.save")
    result = service.run()  # Everything is mocked!

# ❌ Mocking implementation details
def test_calculate(mocker):
    mocker.patch("calculator._internal_helper")  # Private method!

# ✅ Mock at boundaries
def test_service(mocker):
    mocker.patch("service.external_api.call", return_value={"status": "ok"})
    result = service.run()  # Real code runs, only external call mocked
    assert result.processed == True
```

### Test Naming (🔵 Low)

```python
# ❌ Unclear names
def test_1():
def test_user():
def test_it_works():

# ✅ Descriptive names (what is being tested + expected outcome)
def test_create_user_with_valid_email_succeeds():
def test_create_user_with_invalid_email_raises_validation_error():
def test_delete_user_removes_associated_data():
```

## Test Patterns to Check

### Fixture Usage

**Check that tests use project fixtures:**

```python
# ✅ Reuse shared fixtures
def test_with_db(db_session):  # From conftest.py
    user = User(session=db_session)
    
# ✅ Use tmp_path for file operations
def test_export(tmp_path):
    output_file = tmp_path / "export.csv"
    export_data(output_file)
    assert output_file.exists()
```

### Parameterized Tests

**Suggest when seeing repeated test logic:**

```python
# ❌ Duplicated tests
def test_validate_email_valid():
    assert validate_email("user@example.com") == True
    
def test_validate_email_invalid():
    assert validate_email("invalid") == False

# ✅ Parameterized
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("invalid", False),
    ("", False),
    ("user@.com", False),
])
def test_validate_email(email, expected):
    assert validate_email(email) == expected
```

### Edge Cases

**Check for tests covering:**
- Empty inputs
- None values
- Boundary values
- Large inputs
- Concurrent access (if applicable)

```python
# ✅ Edge cases covered
def test_process_empty_list():
    assert process([]) == []
    
def test_process_none_raises():
    with pytest.raises(TypeError):
        process(None)
        
def test_process_single_item():
    assert process([1]) == [2]
```

## Test Anti-Patterns

### Flaky Tests (🟠 High)

**Flag tests that:**
- Use `time.sleep()` for synchronization
- Depend on current time
- Have race conditions

```python
# ❌ Flaky - timing dependent
def test_async_operation():
    start_operation()
    time.sleep(2)  # Might not be enough!
    assert operation_complete()

# ✅ Use proper synchronization
def test_async_operation():
    start_operation()
    wait_for_completion(timeout=5)  # Explicit wait with timeout
    assert operation_complete()
```

### Testing Implementation, Not Behavior (🟡 Moderate)

```python
# ❌ Tests implementation details
def test_user_service(mocker):
    mock_repo = mocker.patch("service.user_repository")
    service.get_user(1)
    mock_repo.find_by_id.assert_called_once_with(1)  # Brittle!

# ✅ Tests behavior
def test_user_service(db_session):
    user = create_test_user(db_session, id=1)
    result = service.get_user(1)
    assert result.id == 1
    assert result.name == user.name
```

## Testing Checklist

- [ ] New code has corresponding tests
- [ ] Tests have meaningful assertions
- [ ] Tests are independent (no shared state)
- [ ] External services properly mocked
- [ ] Edge cases covered
- [ ] No flaky tests (time-dependent, order-dependent)
- [ ] Test names describe what is tested
- [ ] Fixtures reused from conftest.py

## Output Format

```markdown
### Testing
- 🟠 [HIGH] tests/test_service.py:45 - Test has no assertions
  - Test will always pass regardless of behavior
  - 💡 Add: `assert result.status == "success"`

- 🟠 [HIGH] src/processor.py - No tests for new function `process_batch()`
  - Function added without test coverage
  - 💡 Create `tests/test_processor.py:test_process_batch_*`

- 🟡 [MODERATE] tests/test_api.py:78 - Flaky test using time.sleep()
  - May fail intermittently under load
  - 💡 Use `wait_for_condition()` or async/await
```
