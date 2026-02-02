# Architecture Review

## Core Principle: Separation of Concerns

Code should be organized into distinct layers. Violations occur when code crosses boundaries.

## Layer Model

```
Presentation (UI/API) → Business Logic (Domain) → Data Access (Infrastructure)
```

**Rules:**
- Pure/algorithm layers: NO database, HTTP, file I/O, or env vars
- Data layers: NO business rules or presentation formatting
- Dependencies flow inward only

## Orchestration vs Business Logic (🟠 High)

For streaming/pipeline systems:

| Layer | Allowed | Forbidden |
|-------|---------|-----------|
| Orchestration (pipelines/) | Bytewax, Kafka, Pydantic, config | Business algorithms |
| Business Logic (packages/ds-library/) | Pure Python, NumPy, dataclasses | Bytewax, Kafka, Pydantic, SQLAlchemy |

**Test:** Can this function be unit-tested without infrastructure mocks?
- YES → belongs in business logic layer
- NO → review if infrastructure can be abstracted

```python
# ✅ GOOD: Pure function in ds-library
def detect_anomaly(value: float, threshold: float) -> AnomalyResult | None:
    if value > threshold:
        return AnomalyResult(type="EXCEEDED", value=value)
    return None

# Orchestration layer handles schema mapping separately
def _map_to_pydantic(result: AnomalyResult) -> AnomalyRecord:
    return AnomalyRecord(**asdict(result))
```

## Common Violations

| Issue | Severity | Fix |
|-------|----------|-----|
| DB access in utility layer | 🟠 High | Move to data-access, pass data to pure functions |
| Business logic in API routes | 🟠 High | Extract to domain layer |
| Circular imports | 🟠 High | Extract shared code to third module |
| God class (>500 lines, >20 methods) | 🟡 Moderate | Split into focused modules |

## Checklist

- [ ] Pure layers have no infrastructure imports
- [ ] Dependencies flow inward (presentation → business → data)
- [ ] No circular imports between modules
- [ ] Files under 500 lines
