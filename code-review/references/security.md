# Security Review

## Critical Issues (🔴 Always Flag)

### Hardcoded Secrets
```python
# ❌ password = "admin123"; api_key = "sk-1234..."; db_url = "postgres://user:pass@host"
# ✅ password = os.environ["DB_PASSWORD"]
```

### SQL Injection
```python
# ❌ f"SELECT * FROM users WHERE id = {user_id}"
# ✅ cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Command Injection
```python
# ❌ subprocess.run(f"ls {user_path}", shell=True)
# ✅ subprocess.run(["ls", user_path], shell=False)
```

### Path Traversal
```python
# ❌ open(f"/uploads/{filename}")  # Could be "../../../etc/passwd"
# ✅ path = (Path("/uploads") / filename).resolve()
#    if not path.is_relative_to(Path("/uploads")): raise ValueError
```

### Insecure Deserialization
```python
# ❌ pickle.loads(user_input); yaml.load(user_input)
# ✅ json.loads(user_input); yaml.safe_load(user_input)
```

## High Priority (🟠)

| Issue | Detection | Fix |
|-------|-----------|-----|
| Sensitive data in logs | `logger.*password\|secret\|token` | Redact before logging |
| Missing auth checks | Routes without `@require_auth` | Add decorator |
| Weak password hashing | `hashlib.md5`, `hashlib.sha1` | Use `bcrypt` or `argon2` |
| Random for security | `import random` for tokens | Use `secrets` module |

## Checklist

- [ ] No hardcoded secrets
- [ ] All SQL queries parameterized
- [ ] User input validated/sanitized
- [ ] File paths validated against base directory
- [ ] No pickle/unsafe YAML with untrusted data
- [ ] Sensitive data not logged
- [ ] Auth checks on all endpoints
