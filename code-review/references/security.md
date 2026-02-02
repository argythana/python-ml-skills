# Security Review Checklist

## SQL Injection (Critical)

```python
# BAD: String interpolation
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# BAD: String concatenation
query = "SELECT * FROM users WHERE name = '" + name + "'"

# GOOD: Parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# GOOD: ORM with proper filtering
User.query.filter_by(id=user_id).first()
```

## Command Injection (Critical)

```python
# BAD: Shell=True with user input
subprocess.run(f"ls {user_path}", shell=True)

# BAD: os.system with user input
os.system(f"convert {filename} output.png")

# GOOD: List arguments, no shell
subprocess.run(["ls", user_path], shell=False)

# GOOD: shlex.quote for unavoidable shell
subprocess.run(f"ls {shlex.quote(user_path)}", shell=True)
```

## Hardcoded Secrets (Critical)

```python
# BAD
password = "admin123"
api_key = "sk-1234567890abcdef"
db_url = "postgresql://user:password@host/db"

# GOOD: Environment variables
password = os.environ["DB_PASSWORD"]
api_key = os.environ.get("API_KEY")

# GOOD: Secrets manager
from aws_secretsmanager import get_secret
api_key = get_secret("my-api-key")
```

## Path Traversal (Critical)

```python
# BAD: Direct path concatenation
file_path = f"/uploads/{filename}"
with open(file_path) as f:
    return f.read()  # User could pass "../../../etc/passwd"

# GOOD: Validate and sanitize
from pathlib import Path

base_dir = Path("/uploads").resolve()
file_path = (base_dir / filename).resolve()

if not file_path.is_relative_to(base_dir):
    raise ValueError("Invalid path")
```

## Insecure Deserialization (Critical)

```python
# BAD: Pickle with untrusted data
data = pickle.loads(user_input)  # Remote code execution!

# BAD: YAML unsafe load
config = yaml.load(user_input)  # Can execute arbitrary Python

# GOOD: Safe loaders
config = yaml.safe_load(user_input)
data = json.loads(user_input)
```

## Weak Cryptography (High)

```python
# BAD: Weak hashing
password_hash = hashlib.md5(password.encode()).hexdigest()

# BAD: Hardcoded IV/salt
iv = b"1234567890123456"

# BAD: Using random instead of secrets
token = random.randint(0, 999999)

# GOOD: Proper password hashing
from passlib.hash import bcrypt
password_hash = bcrypt.hash(password)

# GOOD: Secure token generation
import secrets
token = secrets.token_urlsafe(32)
```

## Sensitive Data Exposure (High)

```python
# BAD: Logging sensitive data
logger.info(f"User login: {username}, password: {password}")

# GOOD: Redact sensitive fields
logger.info(f"User login: {username}")
```

## Missing Auth (High)

```python
# BAD: No authorization check
@app.route("/admin/users")
def list_users():
    return User.query.all()

# GOOD: With authorization
@app.route("/admin/users")
@require_role("admin")
def list_users():
    return User.query.all()
```

## Security Checklist

- [ ] No hardcoded secrets
- [ ] All SQL queries parameterized
- [ ] User input validated/sanitized
- [ ] File paths validated
- [ ] No dangerous deserialization
- [ ] Sensitive data not logged
- [ ] Auth checks on all endpoints
- [ ] Secure random generation
