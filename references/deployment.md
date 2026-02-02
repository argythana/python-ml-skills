# Deployment Review Checklist

## Required Files

| Component | Required Files |
|-----------|---------------|
| Pipeline | `Dockerfile`, `helm/Chart.yaml`, `helm/values.yaml` |
| Service | `Dockerfile`, `docker-compose.yml` or Helm chart |
| Batch Job | `Dockerfile`, job manifest or Airflow DAG |

## Dockerfile Best Practices (Moderate)

```dockerfile
# BAD: Running as root
USER root
CMD ["python", "app.py"]

# GOOD: Non-root user
USER appuser
CMD ["python", "app.py"]

# BAD: No .dockerignore
COPY . /app  # Copies .git, __pycache__

# GOOD: Explicit copies
COPY requirements.txt /app/
COPY src/ /app/src/

# BAD: Not pinning versions
FROM python:latest
RUN pip install flask

# GOOD: Pinned versions
FROM python:3.11-slim
RUN pip install flask==2.3.0
```

## Helm/Kubernetes

```yaml
# BAD: Missing resource limits
containers:
  - name: app
    image: myapp:latest

# GOOD: With limits and health checks
containers:
  - name: app
    image: myapp:v1.2.3
    resources:
      requests:
        memory: "256Mi"
        cpu: "100m"
      limits:
        memory: "512Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
```

## Environment Variables

```python
# BAD: Required env var without fallback
db_host = os.environ["DATABASE_HOST"]  # Crashes if not set

# GOOD: With fallback and documentation
# DATABASE_HOST: PostgreSQL host (default: localhost)
db_host = os.environ.get("DATABASE_HOST", "localhost")
```

## Configuration Files

```yaml
# BAD: Hardcoded secrets
database:
  host: prod-db.internal
  password: supersecret123

# GOOD: Environment variable references
database:
  host: ${DATABASE_HOST}
  password: ${DATABASE_PASSWORD}
```

## Database Migrations (Critical)

```sql
-- BAD: Locks table for duration
ALTER TABLE users ADD COLUMN email VARCHAR(255) NOT NULL;

-- GOOD: Safe migration pattern
-- Step 1: Add nullable column
ALTER TABLE users ADD COLUMN email VARCHAR(255);
-- Step 2: Backfill data
-- Step 3: Add constraint
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- BAD: Index without CONCURRENTLY
CREATE INDEX idx_users_email ON users(email);

-- GOOD: Non-blocking index (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

## Version Tagging

```dockerfile
# BAD: Using latest
FROM python:latest
image: myapp:latest

# GOOD: Specific versions
FROM python:3.11.4-slim
image: myapp:v1.2.3  # Or git SHA
```

## Observability

### Logging
```python
# BAD: Print statements
print(f"Processing order {order_id}")

# BAD: Unstructured logging
logger.info(f"Processing order {order_id}")

# GOOD: Structured logging
logger.info("Processing order", extra={"order_id": order_id, "user_id": user_id})
```

### Health Checks
Every service needs:
- Liveness endpoint (`/health`)
- Readiness endpoint (`/ready`)

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] Docker image builds
- [ ] Helm chart lints cleanly
- [ ] Database migrations tested
- [ ] Feature flags configured

### Post-Deployment
- [ ] Monitoring dashboards updated
- [ ] Alerts configured
- [ ] Runbook updated
- [ ] Rollback plan documented
