# Code Quality Review

## Automated Checks

See [tooling.md](tooling.md) for ruff, vulture, mypy commands.

## Complexity (🟡 Moderate)

| Metric | Threshold |
|--------|-----------|
| Function lines | >50 |
| Cyclomatic complexity | >10 |
| Nesting depth | >4 |
| Parameters | >5 |

```python
# ❌ Too complex - deeply nested, too many params
def process(order, user, payment, shipping, discount, tax, currency, notify):
    if order:
        if user:
            if payment: ...

# ✅ Refactored into focused functions
def process_order(order: Order) -> OrderResult:
    return OrderResult(process_payment(order), arrange_shipping(order))
```

## Error Handling (🟠 High)

```python
# ❌ except:; except Exception: return None  # Swallows everything
# ✅ except FileNotFoundError: logger.warning(...); return default
# ✅ except PermissionError as e: raise ConfigError(...) from e
```

## Type Hints (🟡 Moderate for public APIs)

```python
# ❌ def calculate(items, rate): ...
# ✅ def calculate(items: list[Item], rate: float) -> float: ...
```

## Configuration Validation

```python
# ❌ config["timeout"]  # No validation
# ✅ class Settings(BaseModel):
#        timeout: int = Field(default=30, gt=0)
```

## Performance

```python
# ❌ for item in items: config = load_config()  # Loads every iteration
# ✅ config = load_config(); for item in items: process(item, config)

# ❌ result = ""; for x in items: result += str(x)  # O(n²)
# ✅ result = "".join(str(x) for x in items)
```

## Checklist

- [ ] Functions under 50 lines
- [ ] No bare `except:` clauses
- [ ] Type hints on public functions
- [ ] No repeated expensive operations in loops
- [ ] Pydantic for config validation
