# Documentation Review

## Docstrings (🟡 Moderate for public APIs)

```python
def calculate_shipping(weight: float, destination: str) -> float:
    """Calculate shipping cost.

    Args:
        weight: Package weight in kg.
        destination: Zone code (e.g., "US-WEST").

    Returns:
        Shipping cost in USD.

    Raises:
        ValueError: If destination unknown.
    """
```

### Common Issues

| Issue | Severity | Fix |
|-------|----------|-----|
| Docstring doesn't match signature | 🟠 High | Update to reflect actual params/return |
| Missing docstring on public function | 🟡 Moderate | Add Google-style docstring |
| Outdated parameter names | 🟠 High | Rename to match code |

## README Requirements

Every package/pipeline should have:
- Purpose and scope
- Installation/setup
- Quick start example
- Link to detailed docs (if any)

**Verify examples actually work:** imports resolve, signatures match, output is accurate.

## Discoverability (🟡 Moderate)

New docs must be linked from an index:
- `docs/` files → link from `docs/README.md`
- Package docs → link from package README

**Flag orphan documentation** that isn't linked anywhere.

## Checklist

- [ ] Public functions have docstrings
- [ ] Docstrings match signatures
- [ ] README examples are runnable
- [ ] New docs linked from index
