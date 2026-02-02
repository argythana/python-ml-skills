# Documentation Review Checklist

## Public APIs Must Have Docstrings (Moderate)

```python
# BAD: Missing docstring
def calculate_shipping(weight, destination):
    return base_rate * weight + zone_rates[destination]

# GOOD: Complete docstring (Google style)
def calculate_shipping(weight: float, destination: str) -> float:
    """Calculate shipping cost based on weight and destination.

    Args:
        weight: Package weight in kilograms.
        destination: Destination zone code (e.g., "US-WEST", "EU").

    Returns:
        Total shipping cost in USD.

    Raises:
        ValueError: If weight is negative or destination is unknown.

    Example:
        >>> calculate_shipping(2.5, "US-WEST")
        12.50
    """
    return base_rate * weight + zone_rates[destination]
```

## Docstring Accuracy (High)

Flag when docstrings don't match function signatures:

```python
# BAD: Parameter name mismatch
def process(data, validate=True):
    """Process the input data.

    Args:
        data: Input data to process.
        strict: Whether to use strict mode.  # Wrong name!
    """

# BAD: Missing parameter
def fetch(url, timeout=30):
    """Fetch data from URL.

    Args:
        url: The URL to fetch.
        # Missing timeout!
    """
```

**Check with:** `darglint --docstring-style google src/`

## Class Documentation

```python
class OrderProcessor:
    """Processes customer orders through the fulfillment pipeline.

    This class handles order validation, payment processing, and
    shipping coordination.

    Attributes:
        payment_gateway: The payment processor instance.
        shipping_provider: The shipping service instance.

    Example:
        >>> processor = OrderProcessor(gateway, shipping)
        >>> result = processor.process(order)
        >>> print(result.status)
        'completed'
    """
```

## README Requirements (Moderate)

Every package should have a README with:
- Purpose and scope
- Installation instructions
- Quick start example
- Link to detailed docs

Flag missing READMEs for `packages/*/`, `pipelines/*/`, `services/*/`

## README Code Examples Must Work

Verify that:
- Import statements are correct
- Function signatures match actual code
- Examples produce expected output

```markdown
# BAD: Outdated import
from mypackage import process_data  # Function was renamed!

# BAD: Wrong signature
result = process(data, strict=True)  # Parameter removed!
```

## Code Comments

Good comments explain WHY, not WHAT:

```python
# BAD: Useless comment
# Increment counter by 1
counter += 1

# GOOD: Explains why
# Rate limit: max 100 requests per minute per API guidelines
counter += 1
if counter >= 100:
    time.sleep(60)
```

## Outdated Comments (Moderate)

Flag comments that:
- Reference removed code
- Describe old behavior
- Have TODO items from years ago

```python
# BAD
# TODO: Remove this hack after Python 2 support dropped (2020)
if sys.version_info[0] == 2:  # Still present in 2024!
```

## Documentation Checklist

- [ ] Public functions have docstrings
- [ ] Docstrings match function signatures
- [ ] README exists for packages
- [ ] README examples are runnable
- [ ] Comments explain why, not what
- [ ] No outdated TODO comments
- [ ] Config options documented
