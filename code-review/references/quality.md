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

## Degenerate-Input & Aggregate Correctness (High)

A degenerate or absent value coerced to a real value is the costliest class of
miss: it returns a *plausible-but-wrong* number with no exception. Check any
aggregate, ranking, or metric path for: absent key / null / non-object / empty
string / empty set / zero count / single distinct class silently becoming a
`0.0`, an `""`, or a divisor.

```python
# BAD: a missing/uncastable score coerced to 0.0 gets ranked as a real value,
# and a zero denominator divides — one bad row poisons the whole aggregate
score = float(row.get("proba") or 0.0)
accuracy = verdict_true / rows_evaluated  # rows_evaluated may be 0

# GOOD: void the degenerate input (drop/NaN/raise), guard the divisor
if not is_finite(score):        # excluded, never zero-ranked
    continue
if rows_evaluated <= 0:
    raise ValueError("empty slice — corrupted statistics, not a quiet window")
```

- absent vs present-but-invalid must be distinguished (an absent key may be a
  real 0; a present-but-uncastable value is a data fault that must void the row)
- when logic is re-implemented (a port, a second backend, a vectorized/SQL
  rewrite), it must re-satisfy the ORIGINAL path's degenerate-case invariants —
  rewrites silently regress them

## Scope & Invariant Correctness (High)

- a slice/tenant/contract-scoped fact computed once at a union/global scope, or
  keyed on too coarse an identity (`model` where the real key is
  `(model, version)`), collapses distinct things — invisible until a second
  instance exists
- a branch gated on a config/flag PROXY (`window_days is None`) instead of the
  real invariant it stands for (`end - start == 1 day`)
- a fault-exclusion branch that emits no operational signal — the failure is
  visible only as a log line or a chart gap; emit an always-present count
  (legible at zero) so a spike is detectable

## Code Duplication (Moderate)

Flag duplicate code blocks >10 lines. Also flag logic re-implemented in
parallel (two backends, a mirror helper) with NO single source of truth: they
drift (e.g. one falls through on `""`, the other on `None`) and diverge
silently. Prefer one shared definition both paths call.

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
