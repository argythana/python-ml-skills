# Architecture Review Checklist

## Layer Violations (Critical)

Pure/algorithm code must NOT contain:
- Database queries or ORM calls
- HTTP requests or API calls
- File I/O operations
- Environment variable access
- Logging with side effects

```python
# BAD: Business logic with database access
def calculate_discount(user_id):
    user = db.query(User).filter_by(id=user_id).first()
    return user.total_purchases * 0.1

# GOOD: Pure function, data passed in
def calculate_discount(total_purchases: float) -> float:
    return total_purchases * 0.1
```

## Dependency Direction (High)

Dependencies flow inward only:
- Presentation → Business → Data ✓
- Data → Business ✗ (violation)

Check imports at top of file - are they appropriate for this layer?

## God Classes/Modules (Moderate)

Flag files exceeding:
- >500 lines of code
- >20 methods in a class
- >10 dependencies imported

Suggest splitting into focused modules.

## Circular Dependencies (Critical)

```python
# module_a.py
from module_b import B  # imports module_b

# module_b.py
from module_a import A  # imports module_a ← Circular!
```

**Detect:** `pydeps --show-cycles src/`

**Fix:**
- Extract shared code to a third module
- Use dependency injection
- Invert the dependency

## Architecture Smells

| Smell | Indicator | Severity |
|-------|-----------|----------|
| Feature Envy | Method uses more data from another class | Moderate |
| Shotgun Surgery | One change requires editing many files | Moderate |
| Divergent Change | One file changes for multiple reasons | High |
| Inappropriate Intimacy | Classes know too much internals | Moderate |

## Output Format

```markdown
### Architecture
- 🔴 [CRITICAL] src/utils/helpers.py:45 - Database access in utility layer
  - Layer violation: utilities should be pure functions
  - Fix: Move query to `data_access/user_repository.py`

- 🟠 [HIGH] src/api/routes.py:120 - Business logic in route handler
  - Discount calculation should be in domain layer
  - Fix: Extract to `domain/pricing.py:calculate_discount()`
```
