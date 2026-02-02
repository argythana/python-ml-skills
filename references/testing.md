# Testing Review Checklist

## Coverage Requirements

New code must have tests:
- Unit tests for business logic (90% coverage)
- Integration tests for data access (80% coverage)
- E2E tests for critical user flows

## Tests Must Have Assertions (High)

```python
# BAD: No assertion
def test_process_data():
    result = process_data(input_data)
    # Test always passes!

# BAD: Weak assertion
def test_process_data():
    result = process_data(input_data)
    assert result  # Only checks truthiness

# GOOD: Meaningful assertions
def test_process_data():
    result = process_data(input_data)
    assert result.status == "success"
    assert result.count == 5
    assert "expected_key" in result.data
```

## Test Isolation (High)

Tests must not depend on execution order or share mutable state.

```python
# BAD: Shared state
class TestUser:
    user = None  # Shared across tests!

    def test_create(self):
        self.user = User.create(name="test")

    def test_delete(self):
        self.user.delete()  # Depends on test_create!

# GOOD: Independent tests
class TestUser:
    def test_create(self):
        user = User.create(name="test")
        assert user.id is not None

    def test_delete(self):
        user = User.create(name="test")
        user.delete()
        assert User.find(user.id) is None
```

## Proper Mocking (Moderate)

```python
# BAD: Over-mocking
def test_service(mocker):
    mocker.patch("service.validate")
    mocker.patch("service.process")
    mocker.patch("service.save")
    result = service.run()  # Everything mocked!

# BAD: Mocking implementation details
def test_calculate(mocker):
    mocker.patch("calculator._internal_helper")  # Private!

# GOOD: Mock at boundaries only
def test_service(mocker):
    mocker.patch("service.external_api.call", return_value={"status": "ok"})
    result = service.run()  # Real code runs
    assert result.processed == True
```

## Fixture Usage

```python
# GOOD: Use tmp_path for file operations
def test_export(tmp_path):
    output_file = tmp_path / "export.csv"
    export_data(output_file)
    assert output_file.exists()

# GOOD: Reuse shared fixtures
def test_with_db(db_session):  # From conftest.py
    user = User(session=db_session)
```

## Parameterized Tests

```python
# BAD: Duplicated tests
def test_validate_email_valid():
    assert validate_email("user@example.com") == True

def test_validate_email_invalid():
    assert validate_email("invalid") == False

# GOOD: Parameterized
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("invalid", False),
    ("", False),
    ("user@.com", False),
])
def test_validate_email(email, expected):
    assert validate_email(email) == expected
```

## Flaky Tests (High)

```python
# BAD: Timing dependent
def test_async_operation():
    start_operation()
    time.sleep(2)  # Might not be enough!
    assert operation_complete()

# GOOD: Proper synchronization
def test_async_operation():
    start_operation()
    wait_for_completion(timeout=5)
    assert operation_complete()
```

## Test Naming (Low)

```python
# BAD
def test_1():
def test_user():
def test_it_works():

# GOOD: Descriptive
def test_create_user_with_valid_email_succeeds():
def test_create_user_with_invalid_email_raises_validation_error():
def test_delete_user_removes_associated_data():
```

## Edge Cases

Tests should cover:
- Empty inputs
- None values
- Boundary values
- Large inputs
- Concurrent access (if applicable)

```python
def test_process_empty_list():
    assert process([]) == []

def test_process_none_raises():
    with pytest.raises(TypeError):
        process(None)

def test_process_single_item():
    assert process([1]) == [2]
```

## Testing Checklist

- [ ] New code has corresponding tests
- [ ] Tests have meaningful assertions
- [ ] Tests are independent (no shared state)
- [ ] External services properly mocked
- [ ] Edge cases covered
- [ ] No flaky tests (time/order dependent)
- [ ] Test names describe what is tested
- [ ] Fixtures reused from conftest.py
