# Deployment Review Checklist

## Core Principle: Code Must Be Deployable

Changes that can't be deployed safely are incomplete.

## Infrastructure Completeness

### Required Files for Deployable Components

**Pipelines/Services need:**

| Component | Required Files |
|-----------|---------------|
| Pipeline | `Dockerfile`, `helm/Chart.yaml`, `helm/values.yaml` |
| Service | `Dockerfile`, `docker-compose.yml` or Helm chart |
| Batch Job | `Dockerfile`, job manifest or Airflow DAG |

**Flag missing infrastructure:**
```markdown
🟠 [HIGH] New pipeline `pipelines/data-sync/` missing:
- [ ] Dockerfile
- [ ] helm/values.yaml
```

### Dockerfile Best Practices (🟡 Moderate)

**Check for:**

```dockerfile
# ❌ Running as root
USER root
CMD ["python", "app.py"]

# ✅ Non-root user
USER appuser
CMD ["python", "app.py"]

# ❌ No .dockerignore
COPY . /app  # Copies everything including .git, __pycache__

# ✅ With .dockerignore or explicit copies
COPY requirements.txt /app/
COPY src/ /app/src/

# ❌ Not pinning versions
FROM python:latest
RUN pip install flask

# ✅ Pinned versions
FROM python:3.11-slim
RUN pip install flask==2.3.0
```

### Helm/Kubernetes Checks

**Verify:**
- Resource limits set (CPU, memory)
- Health checks defined (liveness, readiness)
- Secrets not hardcoded in values.yaml
- Environment variables documented

```yaml
# ❌ Missing resource limits
containers:
  - name: app
    image: myapp:latest

# ✅ With limits
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
```

## Configuration Management

### Environment Variables

**Check that:**
- New env vars are documented
- Defaults are sensible
- Secrets use proper injection

```python
# ❌ Required env var without documentation
db_host = os.environ["DATABASE_HOST"]  # Will crash if not set

# ✅ With fallback and documentation
# DATABASE_HOST: PostgreSQL host (default: localhost)
db_host = os.environ.get("DATABASE_HOST", "localhost")
```

### Configuration Files

**Verify:**
- Sample configs provided (`.env.example`)
- Production configs use env vars, not hardcoded values
- Sensitive values not committed

```yaml
# ❌ Hardcoded in config
database:
  host: prod-db.internal
  password: supersecret123

# ✅ Environment variable references
database:
  host: ${DATABASE_HOST}
  password: ${DATABASE_PASSWORD}
```

## Database Migrations

### Migration Safety (🔴 Critical)

**Flag dangerous migrations:**

```sql
-- ❌ Locks table for duration
ALTER TABLE users ADD COLUMN email VARCHAR(255) NOT NULL;

-- ✅ Safe migration (add nullable, backfill, then add constraint)
ALTER TABLE users ADD COLUMN email VARCHAR(255);
-- Backfill script runs...
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
```

**Check for:**
- Migrations are reversible
- Large table changes use batching
- Index creation uses CONCURRENTLY (PostgreSQL)

### Schema Changes

- [ ] Migration file exists for schema changes
- [ ] Down migration provided
- [ ] Migration tested on copy of prod data

## CI/CD Integration

### Pipeline Updates

**When adding new deployable:**
- Jenkinsfile/GitHub Actions updated
- Build steps added
- Deploy steps configured
- Tests run in pipeline

### Version Tagging

```dockerfile
# ❌ Using latest tag
FROM python:latest
image: myapp:latest

# ✅ Specific versions
FROM python:3.11.4-slim
image: myapp:v1.2.3  # Or git SHA
```

## Observability

### Logging

**Check that new code has:**
- Structured logging (JSON format in production)
- Appropriate log levels
- Request tracing (correlation IDs)

```python
# ❌ Print statements
print(f"Processing order {order_id}")

# ❌ Unstructured logging
logger.info(f"Processing order {order_id}")

# ✅ Structured logging
logger.info("Processing order", extra={"order_id": order_id, "user_id": user_id})
```

### Metrics

**For new services/endpoints:**
- Request rate metrics
- Error rate metrics
- Latency metrics

### Health Checks

**Every service needs:**
- Liveness endpoint (`/health`)
- Readiness endpoint (`/ready`)

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] Docker image builds successfully
- [ ] Helm chart lints cleanly
- [ ] Database migrations tested
- [ ] Feature flags configured (if applicable)

### Post-Deployment
- [ ] Monitoring dashboards updated
- [ ] Alerts configured
- [ ] Runbook updated
- [ ] Rollback plan documented

## Output Format

```markdown
### Deployment
- 🟠 [HIGH] pipelines/new-service/ - Missing infrastructure
  - No Dockerfile found
  - No Helm chart found
  - 💡 Add Dockerfile and helm/ directory

- 🟡 [MODERATE] docker/Dockerfile:15 - Running as root
  - Container runs with root privileges
  - 💡 Add `USER appuser` after installing dependencies

- 🔵 [LOW] helm/values.yaml - No resource limits
  - Pod has no memory/CPU limits set
  - 💡 Add resources.limits section

## Deployment Gaps Summary

For this PR to be deployable, address:
1. Create Dockerfile for new pipeline
2. Add Helm chart with values.yaml
3. Update Jenkinsfile with build/deploy stages
4. Document new environment variables in .env.example
```
