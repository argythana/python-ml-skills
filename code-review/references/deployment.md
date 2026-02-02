# Deployment Review

## Infrastructure Completeness (🟠 High)

New pipelines/services need:
- `Dockerfile`
- `helm/Chart.yaml` + `values.yaml`
- CI/CD pipeline config

## Dockerfile Best Practices

```dockerfile
# ❌ FROM python:latest; USER root; COPY . /app
# ✅ FROM python:3.11-slim
#    USER appuser
#    COPY requirements.txt /app/
```

| Issue | Severity |
|-------|----------|
| Running as root | 🟡 Moderate |
| Unpinned versions | 🟡 Moderate |
| No .dockerignore | 🔵 Low |

## Helm/Kubernetes

```yaml
# ✅ Required: resource limits + health checks
resources:
  requests: { memory: "256Mi", cpu: "100m" }
  limits: { memory: "512Mi", cpu: "500m" }
livenessProbe:
  httpGet: { path: /health, port: 8080 }
```

## Configuration

```python
# ❌ db_host = os.environ["DATABASE_HOST"]  # Crashes if unset
# ✅ db_host = os.environ.get("DATABASE_HOST", "localhost")
```

**Multi-environment pattern:**
- Cloud sources: `database`, `minio`
- Local variants: `database_local`, `minio_local`
- Env var namespacing: `DATABASE_HOST` vs `DATABASE_LOCAL_HOST`

## Migrations (🔴 Critical for data safety)

```sql
-- ❌ ALTER TABLE users ADD COLUMN email VARCHAR(255) NOT NULL;  -- Locks table
-- ✅ Add nullable → backfill → add constraint
```

## Checklist

- [ ] Dockerfile exists with non-root user
- [ ] Helm chart has resource limits
- [ ] New env vars documented in `.env.example`
- [ ] Migrations are reversible
- [ ] Health endpoints defined
