# Documentation Review Checklist

## Core Principle: Documentation Should Be Accurate and Discoverable

Documentation that is wrong or outdated is worse than no documentation.

## Docstring Requirements

### Public APIs Must Have Docstrings (🟡 Moderate)

```python
# ❌ Missing docstring
def calculate_shipping(weight, destination):
    return base_rate * weight + zone_rates[destination]

# ✅ Complete docstring (Google style)
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

### Docstring Accuracy (🟠 High)

**Flag when:**
- Docstring doesn't match function signature
- Documented parameters don't exist
- Return type is wrong
- Missing documented exceptions

```python
# ❌ Docstring doesn't match signature
def process(data, validate=True):
    """Process the input data.
    
    Args:
        data: Input data to process.
        strict: Whether to use strict mode.  # Wrong parameter name!
    """

# ❌ Missing documented parameter
def fetch(url, timeout=30):
    """Fetch data from URL.
    
    Args:
        url: The URL to fetch.
        # Missing timeout parameter!
    """
```

### Class Documentation

```python
# ✅ Well-documented class
class OrderProcessor:
    """Processes customer orders through the fulfillment pipeline.
    
    This class handles order validation, payment processing, and
    shipping coordination. It maintains state through the order
    lifecycle.
    
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

## README Requirements

### Package READMEs (🟡 Moderate)

Every package should have a README with:
- Purpose and scope
- Installation instructions
- Quick start example
- Link to detailed docs

**Flag missing READMEs for:**
- `packages/*/`
- `pipelines/*/`
- `services/*/`

### README Code Examples Must Work

**Verify that:**
- Import statements are correct
- Function signatures match actual code
- Examples produce expected output

```markdown
# ❌ README example with wrong import
from mypackage import process_data  # Function was renamed!

# ❌ README example with outdated signature
result = process(data, strict=True)  # Parameter removed!
```

## Code Comments

### When Comments Are Needed

**Good comments explain WHY, not WHAT:**

```python
# ❌ Useless comment (explains what)
# Increment counter by 1
counter += 1

# ✅ Useful comment (explains why)
# Rate limit: max 100 requests per minute per API guidelines
counter += 1
if counter >= 100:
    time.sleep(60)
```

### Outdated Comments (🟡 Moderate)

**Flag comments that:**
- Reference removed code
- Describe old behavior
- Have TODO items from years ago

```python
# ❌ Outdated comment
# TODO: Remove this hack after Python 2 support is dropped (2020)
if sys.version_info[0] == 2:  # Code still present in 2024!

# ❌ Comment doesn't match code
# Returns None if user not found
def get_user(id):
    return User.query.get(id)  # Actually raises exception!
```

## Documentation Consistency

### Check Code-Documentation Sync

When code changes, verify:
1. **Docstrings updated** - Parameters, returns, exceptions
2. **README examples** - Still work with new API
3. **Config docs** - Reflect actual config options
4. **API docs** - Match implementation

### Cross-Reference Verification

```python
# In documentation: "Use validate_input() from utils module"
# Verify: Does utils.validate_input() actually exist?

# In README: "Set LOG_LEVEL environment variable"
# Verify: Does code actually read LOG_LEVEL?
```

## Documentation Standards

### Markdown Files

- Clear headings hierarchy (H1 > H2 > H3)
- Code blocks with language specified
- Links to related documents
- Table of contents for long documents

### API Documentation

- All public endpoints documented
- Request/response examples
- Error codes explained
- Authentication requirements clear

## Documentation Checklist

- [ ] Public functions have docstrings
- [ ] Docstrings match function signatures
- [ ] README exists for packages
- [ ] README examples are runnable
- [ ] Comments explain why, not what
- [ ] No outdated TODO comments
- [ ] Config options documented
- [ ] New docs linked from index

## Output Format

```markdown
### Documentation
- 🟠 [HIGH] src/api/client.py:45 - Docstring doesn't match signature
  - Documents `timeout` parameter but function has `max_wait`
  - 💡 Update docstring: `max_wait: Maximum wait time in seconds`

- 🟡 [MODERATE] packages/utils/README.md - Example uses outdated API
  - Line 23: `from utils import old_function` - function was renamed
  - 💡 Update to: `from utils import new_function`

- 🔵 [LOW] src/processor.py:78 - Missing docstring on public function
  - `process_batch()` has no documentation
  - 💡 Add docstring explaining purpose, args, and return value
```
