# Chapter 19 sample: Docker, Compose, and Kubernetes for Python Apps

- `catalog-api/` - the service from the chapter
  - `Dockerfile`, `.dockerignore` - two-stage uv build (Listing 19-3)
  - `compose.yaml`, `.env.example` - web, migrate, worker, PostgreSQL 18, Redis 8 (Listing 19-4)
  - `k8s/` - Deployment, Service, ConfigMap, example Secret, migration Job, worker (Listings 19-5, 19-7)
  - `chart/catalog/` - the Helm chart (Listings 19-8, 19-9)
  - `CLAUDE.md`, `.claude/settings.json` - container rules and cluster-safe permissions (Listing 19-2)
- `demos/` - Claude's first Dockerfile (Listing 19-1) and the scripts behind the chapter's outputs
- `tools/k8s_validate.py` - strict validation against the Kubernetes OpenAPI schemas
  (set K8S_OPENAPI_DIR to api/openapi-spec/v3 from kubernetes/kubernetes)
- `tools/minihelm/` - the template stand-in used to render the chart without Helm
- `outputs/` - the real outputs quoted in the chapter

## Getting started

    cd catalog-api
    uv lock                      # once, then commit uv.lock (the Dockerfile uses --locked)
    cp .env.example .env         # and set POSTGRES_PASSWORD
    docker build --check . && docker compose up --build

## What was run here

The app's tests, Ruff and mypy; the Dockerfile built and run with stand-in base images
(registry unreachable) and web dependencies only; Compose validated with `docker compose config`;
manifests and the rendered chart validated against Kubernetes v1.37.2 schemas.
Not run: a Kubernetes cluster, kind, Helm, PostgreSQL, Redis, Celery and Alembic.
