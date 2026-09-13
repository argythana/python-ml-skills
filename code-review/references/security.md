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

## Injection Beyond SQL Values — Query/Filter DSLs

`?`-parameterized SQL values are not the whole surface. Data-derived strings (a
run name, a class label, a model version, any field carrying user/producer
data) interpolated into a DSL that has no in-string escaping are an injection
and silent-breakage risk: SQL *identifiers* (table/column names), MLflow /
search `filter_string`, JSON-path expressions, LDAP filters, regexes, shell.

```python
# BAD: f-string into a filter DSL with no escaping. A stray quote breaks the
# filter and the match silently returns nothing (stale row survives) — or the
# wrong rows. Works today only because values HAPPEN to be quote-free.
runs = client.search_runs(filter_string=f"attributes.run_name = '{run_name}'")

# GOOD: whitelist/validate identifiers; pick the quote char + client-side fallback
if not label.replace("_", "").isalnum():
    raise ValueError(f"non-identifier label {label!r}")
```

Flag any f-string / `.format` / `%` whose result flows into `filter_string=`,
raw SQL text, an identifier position, or a path/DSL expression.

## Security Checklist

- [ ] No hardcoded secrets
- [ ] All SQL queries parameterized (values AND identifiers; plus non-SQL
      query/filter DSLs — MLflow filters, JSON paths — validated/whitelisted)
- [ ] User input validated/sanitized
- [ ] File paths validated
- [ ] No dangerous deserialization
- [ ] Sensitive data not logged
- [ ] Auth checks on all endpoints
- [ ] Secure random generation
