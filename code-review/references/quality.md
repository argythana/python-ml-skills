# Code Quality Review Checklist

## Automated Checks

```bash
# Linting
ruff check --output-format=json <files>

# Dead code detection
vulture --min-confidence=80 <files>

# Type checking
mypy --ignore-missing-imports <files>
```

## Function Complexity (Moderate)

Flag functions that exceed:
- >50 lines of code
- >10 cyclomatic complexity
- >5 levels of nesting
- >7 parameters

```python
# BAD: Too complex
def process_order(order, user, payment, shipping, discount,
                  tax_rate, currency, notify, validate, log):
    if order:
        if user:
            if payment:
                if shipping:
                    # deeply nested...

# GOOD: Refactored
def process_order(order: Order) -> OrderResult:
    validated = validate_order(order)
    payment_result = process_payment(validated)
    shipping_result = arrange_shipping(validated)
    return OrderResult(payment_result, shipping_result)
```

## Error Handling (High)

```python
# BAD: Bare except
try:
    data = load_file(path)
except:
    pass  # Swallows all errors including KeyboardInterrupt!

# BAD: Too broad
try:
    result = api_call()
except Exception:
    return None  # Hides the actual error

# GOOD: Specific exceptions
try:
    data = load_file(path)
except FileNotFoundError:
    logger.warning(f"File not found: {path}")
    return default_data
except PermissionError as e:
    raise ConfigurationError(f"Cannot read {path}") from e
```

## Code Duplication (Moderate)

Flag duplicate code blocks >10 lines.

```python
# BAD: Duplicated logic
def process_user(user):
    if not user.email:
        raise ValueError("Email required")
    if not user.name:
        raise ValueError("Name required")

def process_admin(admin):
    if not admin.email:
        raise ValueError("Email required")  # Duplicated!
    if not admin.name:
        raise ValueError("Name required")

# GOOD: Extract common logic
def validate_person(person):
    if not person.email:
        raise ValueError("Email required")
    if not person.name:
        raise ValueError("Name required")

def process_user(user):
    validate_person(user)
```

## Performance (Moderate)

```python
# BAD: Repeated lookups in loop
for item in items:
    config = load_config()  # Loaded every iteration!
    process(item, config)

# GOOD: Load once
config = load_config()
for item in items:
    process(item, config)

# BAD: String concatenation O(n²)
result = ""
for item in items:
    result += str(item)

# GOOD: Use join
result = "".join(str(item) for item in items)

# BAD: List when generator suffices
total = sum([x * 2 for x in range(1000000)])  # Full list

# GOOD: Generator expression
total = sum(x * 2 for x in range(1000000))  # Memory efficient
```

## Naming Conventions (Low)

```python
# BAD
def ProcessData(inputData):
    MyVariable = inputData

# GOOD
def process_data(input_data):
    my_variable = input_data
```

Python conventions:
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- `_private` prefix for internal use

## Magic Numbers (Low)

```python
# BAD
if user.age >= 18:
    if retry_count < 3:
        time.sleep(0.5)

# GOOD
LEGAL_AGE = 18
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 0.5

if user.age >= LEGAL_AGE:
    if retry_count < MAX_RETRIES:
        time.sleep(RETRY_DELAY_SECONDS)
```

## Quality Metrics

| Metric | Threshold | Severity |
|--------|-----------|----------|
| Function lines | >50 | Moderate |
| Cyclomatic complexity | >10 | Moderate |
| File lines | >500 | Moderate |
| Nesting depth | >4 | Moderate |
| Function parameters | >5 | Low |
| Duplicate blocks | >10 lines | Moderate |
