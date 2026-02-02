# Code Quality Review Checklist

## Automated Checks

### Ruff (Linting)

Run before manual review:
```bash
ruff check --output-format=json <files>
```

Key rule categories:
- **E**: pycodestyle errors
- **W**: pycodestyle warnings
- **F**: pyflakes (unused imports, undefined names)
- **I**: isort (import ordering)
- **B**: bugbear (common bugs)
- **C4**: comprehensions
- **UP**: pyupgrade (modern syntax)

### Dead Code Detection

```bash
vulture --min-confidence=80 <files>
```

Flags:
- Unused functions
- Unused classes
- Unused variables
- Unused imports
- Unreachable code

### Type Checking

```bash
mypy --ignore-missing-imports <files>
```

## Manual Quality Checks

### Function Complexity (🟡 Moderate)

**Flag functions that are:**
- \>50 lines of code
- \>10 cyclomatic complexity
- \>5 levels of nesting
- \>7 parameters

```python
# ❌ Too complex - needs refactoring
def process_order(order, user, payment, shipping, discount, 
                  tax_rate, currency, notify, validate, log):
    if order:
        if user:
            if payment:
                if shipping:
                    # ... deeply nested logic
                    pass

# ✅ Refactored into focused functions
def process_order(order: Order) -> OrderResult:
    validated = validate_order(order)
    payment_result = process_payment(validated)
    shipping_result = arrange_shipping(validated)
    return OrderResult(payment_result, shipping_result)
```

### Code Duplication (🟡 Moderate)

**Flag duplicate code blocks >10 lines**

```python
# ❌ Duplicated logic
def process_user(user):
    if not user.email:
        raise ValueError("Email required")
    if not user.name:
        raise ValueError("Name required")
    # ... process

def process_admin(admin):
    if not admin.email:
        raise ValueError("Email required")  # Duplicated!
    if not admin.name:
        raise ValueError("Name required")   # Duplicated!
    # ... process

# ✅ Extract common logic
def validate_person(person):
    if not person.email:
        raise ValueError("Email required")
    if not person.name:
        raise ValueError("Name required")

def process_user(user):
    validate_person(user)
    # ... process
```

### Naming Conventions (🔵 Low)

**Python conventions:**
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- `_private` prefix for internal use

```python
# ❌ Inconsistent naming
def ProcessData(inputData):  # Should be snake_case
    MyVariable = inputData   # Should be snake_case
    
# ✅ Correct naming
def process_data(input_data):
    my_variable = input_data
```

### Error Handling (🟠 High)

**Flag:**
- Bare `except:` clauses
- `except Exception:` without re-raising
- Silently swallowed exceptions
- Missing error handling on I/O operations

```python
# ❌ Bare except
try:
    data = load_file(path)
except:
    pass  # Swallows all errors including KeyboardInterrupt!

# ❌ Too broad exception
try:
    result = api_call()
except Exception:
    return None  # Hides the actual error

# ✅ Specific exceptions, proper handling
try:
    data = load_file(path)
except FileNotFoundError:
    logger.warning(f"File not found: {path}")
    return default_data
except PermissionError as e:
    raise ConfigurationError(f"Cannot read {path}") from e
```

### Type Hints (🟡 Moderate for public APIs)

**Require type hints for:**
- Public function signatures
- Class attributes
- Return types

```python
# ❌ Missing type hints
def calculate_total(items, tax_rate):
    total = sum(item.price for item in items)
    return total * (1 + tax_rate)

# ✅ With type hints
def calculate_total(items: list[Item], tax_rate: float) -> float:
    total = sum(item.price for item in items)
    return total * (1 + tax_rate)
```

### Magic Numbers/Strings (🔵 Low)

```python
# ❌ Magic numbers
if user.age >= 18:
    if retry_count < 3:
        time.sleep(0.5)

# ✅ Named constants
LEGAL_AGE = 18
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 0.5

if user.age >= LEGAL_AGE:
    if retry_count < MAX_RETRIES:
        time.sleep(RETRY_DELAY_SECONDS)
```

## Performance Considerations (🟡)

### Inefficient Patterns

```python
# ❌ Repeated lookups in loop
for item in items:
    config = load_config()  # Loaded every iteration!
    process(item, config)

# ✅ Load once
config = load_config()
for item in items:
    process(item, config)

# ❌ String concatenation in loop
result = ""
for item in items:
    result += str(item)  # O(n²) complexity!

# ✅ Use join
result = "".join(str(item) for item in items)

# ❌ List when generator would suffice
total = sum([x * 2 for x in range(1000000)])  # Creates full list

# ✅ Generator expression
total = sum(x * 2 for x in range(1000000))  # Memory efficient
```

## Quality Metrics Summary

| Metric | Threshold | Severity |
|--------|-----------|----------|
| Function lines | >50 | Moderate |
| Cyclomatic complexity | >10 | Moderate |
| File lines | >500 | Moderate |
| Nesting depth | >4 | Moderate |
| Function parameters | >5 | Low |
| Duplicate blocks | >10 lines | Moderate |

## Output Format

```markdown
### Code Quality
- 🟠 [HIGH] utils/parser.py:89 - Bare except clause
  - Catches all exceptions including SystemExit
  - 💡 Specify exception: `except ValueError:`

- 🟡 [MODERATE] services/processor.py:45 - Function too long (78 lines)
  - Exceeds 50 line threshold
  - 💡 Extract validation logic to `_validate_input()`

- 🔵 [LOW] models/user.py:12 - Magic number
  - Hardcoded value `30` without context
  - 💡 Extract constant: `DEFAULT_TIMEOUT_SECONDS = 30`
```
