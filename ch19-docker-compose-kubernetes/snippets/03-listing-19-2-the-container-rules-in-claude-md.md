## Container rules

- Base image `python:3.13-slim-trixie` in both stages; never `latest`, never alpine.
- Install with `uv sync --locked`; dependencies in their own layer before `COPY .`.
- Runtime stage runs as the `app` user (uid 999) and has no uv, no compilers.
- `CMD` and `ENTRYPOINT` in exec (JSON) form only. One process per container in
  Kubernetes; scale with replicas, not workers.
- Configuration and secrets come from environment variables. Never bake a secret
  into the image, a manifest or values.yaml.
- `/healthz` must not touch the database or Redis; `/readyz` checks both.
- Every container has a memory request and limit, and a CPU request.

## Cluster safety

- Show me `helm template` or `kubectl diff` output before any apply or upgrade.
- Never run `kubectl delete` or `helm uninstall` yourself.
