# Code-Documentation Consistency Checklist

## README Examples vs Actual Code (High)

Check that README code blocks:
- Use correct import paths
- Match current function signatures
- Produce documented output

```markdown
<!-- README.md claims: -->
from mylib import process_data
result = process_data(input, validate=True)

<!-- Verify in code: -->
# 1. Does mylib.process_data exist?
# 2. Does it accept 'validate' parameter?
# 3. Does example actually work?
```

**How to verify:**
```bash
# Extract code blocks and check
grep -A 10 "```python" README.md
grep -r "def process_data" src/
```

## Docstrings vs Function Signatures (High)

```python
# BAD: Docstring-signature mismatch
def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from URL.

    Args:
        url: The URL to fetch
        max_retries: Number of retry attempts  # Wrong!

    Returns:
        str: Response text  # Wrong! Returns dict
    """
```

**Check with:** `darglint src/`

## Config Documentation vs Code

Check that documented env vars exist:

```markdown
<!-- docs/configuration.md says: -->
| Variable | Description |
|----------|-------------|
| LOG_LEVEL | Logging verbosity |
| MAX_WORKERS | Thread pool size |
```

```bash
# Verify these are used:
grep -r "LOG_LEVEL\|MAX_WORKERS" src/
```

## API Documentation vs Implementation

For REST APIs verify:
- Documented endpoints exist
- Request/response schemas match
- Error codes are accurate

```yaml
# OpenAPI spec claims:
/users/{id}:
  get:
    responses:
      200:
        schema: UserResponse
      404:
        description: User not found

# Verify:
# 1. Route exists in code
# 2. Returns UserResponse schema
# 3. Actually returns 404 (not 500) when not found
```

## Architecture Docs vs Code Structure

```markdown
<!-- ARCHITECTURE.md claims: -->
packages/core-lib/  # Pure algorithms, no I/O

<!-- Verify no violations: -->
grep -r "import requests\|import sqlalchemy" packages/core-lib/
```

## Common Consistency Issues

### Renamed Functions/Classes
```python
# Old: process_data()
# New: transform_data()
# But README still references process_data()
```

**Fix:** `grep -r "process_data" docs/ README.md`

### Changed Parameters
```python
# Old: def fetch(url, timeout=30)
# New: def fetch(url, max_wait=30)
# But docstring still says 'timeout'
```

### Moved Modules
```python
# Old: from utils.helpers import validate
# New: from core.validation import validate
# But README has old import
```

### Outdated Examples
```python
# README shows:
result = api.call(data)
print(result.value)

# But now:
result = api.call(data)
print(result.data.value)  # Structure changed!
```

## Consistency Checklist

- [ ] README imports match actual module structure
- [ ] README examples use current function signatures
- [ ] Docstrings match function parameters
- [ ] Docstring return types match actual returns
- [ ] Config docs list all env vars code expects
- [ ] Architecture claims match actual code organization
- [ ] API docs match implemented endpoints
- [ ] Error messages match documented error codes
