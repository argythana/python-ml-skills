# Architecture Review Checklist

## Core Principle: Separation of Concerns

Code should be organized into distinct layers with clear responsibilities. Violations occur when code crosses layer boundaries inappropriately.

## Common Layer Patterns

### Three-Layer Architecture
```
┌─────────────────────────────────────┐
│  Presentation Layer (UI/API)        │  ← Handles HTTP, CLI, UI
├─────────────────────────────────────┤
│  Business Logic Layer (Domain)      │  ← Pure business rules
├─────────────────────────────────────┤
│  Data Access Layer (Infrastructure) │  ← Database, external APIs
└─────────────────────────────────────┘
```

### Package-Based Architecture (Monorepos)
```
packages/
├── core-lib/       # Pure algorithms, no I/O
├── data-access/    # Database, external services
└── app/            # Entry points, configuration
```

## What to Check

### Layer Violations (🔴 Critical)

**Pure/Algorithm Layer** should NOT contain:
- Database queries or ORM calls
- HTTP requests or API calls
- File I/O operations
- Environment variable access
- Logging with side effects

```python
# ❌ BAD: Business logic with database access
def calculate_discount(user_id):
    user = db.query(User).filter_by(id=user_id).first()  # Layer violation!
    return user.total_purchases * 0.1

# ✅ GOOD: Pure function, data passed in
def calculate_discount(total_purchases: float) -> float:
    return total_purchases * 0.1
```

**Data Layer** should NOT contain:
- Business rules or calculations
- Presentation formatting
- Direct framework dependencies (Flask, FastAPI routes)

**Presentation Layer** should NOT contain:
- Direct database access
- Complex business logic
- Data transformation beyond formatting

### Dependency Direction (🟠 High)

Dependencies should flow inward:
- Presentation → Business → Data ✅
- Data → Business ❌ (violation)

Check imports at top of file - are they appropriate for this layer?

### God Classes/Modules (🟡 Moderate)

Flag files exceeding thresholds:
- \>500 lines of code
- \>20 methods in a class
- \>10 dependencies imported

Suggest splitting into focused modules.

### Circular Dependencies (🔴 Critical)

```python
# module_a.py
from module_b import B  # module_a imports module_b

# module_b.py  
from module_a import A  # module_b imports module_a ← Circular!
```

**How to detect:**
```bash
# Use pydeps or similar tool
pydeps --show-cycles src/
```

**How to fix:**
- Extract shared code to a third module
- Use dependency injection
- Invert the dependency

## Architecture Smell Patterns

| Smell | Indicator | Severity |
|-------|-----------|----------|
| Feature Envy | Method uses more data from another class than its own | Moderate |
| Shotgun Surgery | One change requires editing many files | Moderate |
| Divergent Change | One file changes for multiple unrelated reasons | High |
| Inappropriate Intimacy | Classes know too much about each other's internals | Moderate |

## Project-Specific Rules

When reviewing, check if the project has:
- `ARCHITECTURE.md` - Follow documented patterns
- Package READMEs - Respect stated responsibilities
- Import restrictions in `pyproject.toml` or similar

## Review Output Format

```markdown
### Architecture
- 🔴 [CRITICAL] src/utils/helpers.py:45 - Database access in utility layer
  - Layer violation: utilities should be pure functions
  - 💡 Move query to `data_access/user_repository.py`

- 🟠 [HIGH] src/api/routes.py:120 - Business logic in route handler
  - Discount calculation should be in domain layer
  - 💡 Extract to `domain/pricing.py:calculate_discount()`
```
