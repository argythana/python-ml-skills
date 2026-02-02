# Code-Documentation Consistency Checklist

## Core Principle: Code and Docs Must Match

When code changes, documentation must change too. Inconsistency erodes trust.

## What to Cross-Reference

### 1. README Examples vs Actual Code (🟠 High)

**Check that README code blocks:**
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
# Extract code blocks and test them
grep -A 10 "```python" README.md
# Then check against actual imports
grep -r "def process_data" src/
```

### 2. Docstrings vs Function Signatures (🟠 High)

```python
# ❌ Docstring-signature mismatch
def fetch_data(url: str, timeout: int = 30) -> dict:
    """Fetch data from URL.
    
    Args:
        url: The URL to fetch
        max_retries: Number of retry attempts  # Wrong! Should be timeout
    
    Returns:
        str: Response text  # Wrong! Returns dict
    """
```

**Automated check:**
```bash
# Use pydocstyle or darglint
darglint src/
```

### 3. Config Documentation vs Actual Config Options

**Check that documented env vars exist in code:**

```markdown
<!-- docs/configuration.md says: -->
| Variable | Description |
|----------|-------------|
| LOG_LEVEL | Logging verbosity |
| MAX_WORKERS | Thread pool size |
```

```python
# Verify these are actually used:
grep -r "LOG_LEVEL\|MAX_WORKERS" src/
```

### 4. API Documentation vs Implementation

**For REST APIs:**
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

### 5. Architecture Docs vs Code Structure

**Check ARCHITECTURE.md claims match reality:**

```markdown
<!-- ARCHITECTURE.md claims: -->
packages/core-lib/  # Pure algorithms, no I/O

<!-- Verify no violations: -->
grep -r "import requests\|import sqlalchemy" packages/core-lib/
```

## Consistency Verification Steps

### Step 1: Identify Documentation Files

Look for:
- `README.md` in changed directories
- `docs/*.md` files
- Docstrings in changed functions
- API specs (`openapi.yaml`, `swagger.json`)
- Config examples (`.env.example`)

### Step 2: Extract Testable Claims

For each doc file, identify:
- Import statements that should work
- Function calls with specific signatures
- Environment variables that should be read
- File paths that should exist
- API endpoints that should respond

### Step 3: Verify Against Code

```bash
# Check imports exist
python -c "from claimed.module import function"

# Check env vars are read
grep -r "os.environ\|os.getenv" src/ | grep "CLAIMED_VAR"

# Check file paths exist
ls -la claimed/path/file.py
```

## Common Consistency Issues

### Renamed Functions/Classes

```python
# Old: process_data()
# New: transform_data()
# But README still references process_data()
```

**Fix:** Search docs for old name:
```bash
grep -r "process_data" docs/ README.md
```

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

## Output Format

```markdown
### Consistency
- 🟠 [HIGH] README.md:45 - Import path outdated
  - Claims `from utils import process` but module moved to `core.process`
  - 💡 Update to: `from core import process`

- 🟠 [HIGH] src/api/client.py:23 - Docstring parameter mismatch
  - Docstring documents `timeout` but parameter is `max_wait`
  - 💡 Update docstring: `max_wait: Maximum wait time in seconds`

- 🟡 [MODERATE] docs/config.md - Missing env var documentation
  - Code reads `NEW_FEATURE_FLAG` but not documented
  - 💡 Add to config.md: `NEW_FEATURE_FLAG: Enable new feature (default: false)`
```

## Automated Consistency Checks

### Script: Check README Examples
```python
#!/usr/bin/env python
"""Extract and test README code examples."""
import re
import subprocess

def extract_python_blocks(readme_path):
    with open(readme_path) as f:
        content = f.read()
    pattern = r'```python\n(.*?)\n```'
    return re.findall(pattern, content, re.DOTALL)

def test_imports(code_block):
    """Test that imports in code block work."""
    import_lines = [l for l in code_block.split('\n') if l.startswith('from ') or l.startswith('import ')]
    for line in import_lines:
        try:
            exec(line)
        except ImportError as e:
            return f"Failed: {line} - {e}"
    return None
```

### Script: Check Docstring Consistency
```bash
# Use darglint for docstring checking
pip install darglint
darglint --docstring-style google src/
```
