# Security Review Checklist

## Critical Security Issues (🔴 Always Flag)

### 1. Hardcoded Secrets

**Patterns to detect:**
```python
# ❌ Hardcoded credentials
password = "admin123"
api_key = "sk-1234567890abcdef"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ❌ Secrets in connection strings
db_url = "postgresql://user:password@host/db"

# ❌ Private keys in code
private_key = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3...
-----END RSA PRIVATE KEY-----"""
```

**Fix suggestion:**
```python
# ✅ Use environment variables
import os
password = os.environ["DB_PASSWORD"]
api_key = os.environ.get("API_KEY")

# ✅ Or use a secrets manager
from aws_secretsmanager import get_secret
api_key = get_secret("my-api-key")
```

### 2. SQL Injection

**Vulnerable patterns:**
```python
# ❌ String interpolation
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# ❌ String concatenation
query = "SELECT * FROM users WHERE name = '" + name + "'"

# ❌ Format strings
query = "SELECT * FROM users WHERE id = %s" % user_id
cursor.execute(query)
```

**Secure patterns:**
```python
# ✅ Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ✅ ORM with proper filtering
User.query.filter_by(id=user_id).first()

# ✅ SQLAlchemy with bound parameters
session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
```

### 3. Command Injection

**Vulnerable patterns:**
```python
# ❌ Shell=True with user input
import subprocess
subprocess.run(f"ls {user_path}", shell=True)

# ❌ os.system with user input
os.system(f"convert {filename} output.png")
```

**Secure patterns:**
```python
# ✅ Use list arguments, no shell
subprocess.run(["ls", user_path], shell=False)

# ✅ Use shlex.quote for unavoidable shell usage
import shlex
subprocess.run(f"ls {shlex.quote(user_path)}", shell=True)
```

### 4. Path Traversal

**Vulnerable patterns:**
```python
# ❌ Direct path concatenation
file_path = f"/uploads/{filename}"
with open(file_path) as f:
    return f.read()  # User could pass "../../../etc/passwd"
```

**Secure patterns:**
```python
# ✅ Validate and sanitize paths
from pathlib import Path

base_dir = Path("/uploads").resolve()
file_path = (base_dir / filename).resolve()

# Ensure path is within base directory
if not file_path.is_relative_to(base_dir):
    raise ValueError("Invalid path")
```

### 5. Insecure Deserialization

**Dangerous patterns:**
```python
# ❌ Pickle with untrusted data
import pickle
data = pickle.loads(user_input)  # Remote code execution risk!

# ❌ YAML unsafe load
import yaml
config = yaml.load(user_input)  # Can execute arbitrary Python
```

**Secure patterns:**
```python
# ✅ Use safe loaders
import yaml
config = yaml.safe_load(user_input)

# ✅ Use JSON for untrusted data
import json
data = json.loads(user_input)
```

## High Priority Issues (🟠)

### 6. Sensitive Data Exposure

**Check for:**
- Passwords in logs
- PII in error messages
- Tokens in URLs
- Sensitive data in exceptions

```python
# ❌ Logging sensitive data
logger.info(f"User login: {username}, password: {password}")

# ✅ Redact sensitive fields
logger.info(f"User login: {username}")
```

### 7. Missing Authentication/Authorization

**Check that:**
- Endpoints have auth decorators
- Resource ownership is verified
- Role checks are in place

```python
# ❌ No authorization check
@app.route("/admin/users")
def list_users():
    return User.query.all()

# ✅ With authorization
@app.route("/admin/users")
@require_role("admin")
def list_users():
    return User.query.all()
```

### 8. Cryptographic Issues

**Flag these:**
```python
# ❌ Weak hashing for passwords
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ❌ Hardcoded IV/salt
iv = b"1234567890123456"

# ❌ Using random instead of secrets
import random
token = random.randint(0, 999999)
```

**Recommend:**
```python
# ✅ Use proper password hashing
from passlib.hash import bcrypt
password_hash = bcrypt.hash(password)

# ✅ Use secrets module for tokens
import secrets
token = secrets.token_urlsafe(32)
```

## Security Review Checklist

- [ ] No hardcoded secrets
- [ ] All SQL queries parameterized
- [ ] User input validated/sanitized
- [ ] File paths validated
- [ ] No dangerous deserialization
- [ ] Sensitive data not logged
- [ ] Auth checks on all endpoints
- [ ] Secure random generation
- [ ] Dependencies checked for CVEs

## Output Format

```markdown
### Security
- 🔴 [CRITICAL] auth/login.py:23 - Hardcoded API key
  - Credential exposed in source code
  - 💡 Move to environment variable: `os.environ["API_KEY"]`

- 🔴 [CRITICAL] db/queries.py:45 - SQL injection vulnerability
  - User input directly in query string
  - 💡 Use parameterized query: `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
```
