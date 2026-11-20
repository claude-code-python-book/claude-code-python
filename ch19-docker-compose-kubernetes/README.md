# Chapter 19 — Docker, Compose, and Kubernetes for Python Apps

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`ch19-containers-sample`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-listing-19-1-claude-s-first-dockerfile.Dockerfile`](snippets/01-listing-19-1-claude-s-first-dockerfile.Dockerfile) | Listing 19-1: Claude's first Dockerfile | dockerfile | 3. Writing Your First Dockerfile with Claude Code |
| [`02-output.txt`](snippets/02-output.txt) | Output | text | 3. Writing Your First Dockerfile with Claude Code |
| [`03-listing-19-2-the-container-rules-in-claude-md.md`](snippets/03-listing-19-2-the-container-rules-in-claude-md.md) | Listing 19-2: The container rules in CLAUDE.md | markdown | 3. Writing Your First Dockerfile with Claude Code |
| [`04-output.txt`](snippets/04-output.txt) | Output | text | 4. Picking a Base Image: slim vs alpine (and Why Alpine Hurts Python Wheels) |
| [`05-listing-19-3-dockerfile.Dockerfile`](snippets/05-listing-19-3-dockerfile.Dockerfile) | Listing 19-3: Dockerfile | dockerfile | 5. Multi-Stage Builds with uv |
| [`06-output.txt`](snippets/06-output.txt) | Output | text | 5. Multi-Stage Builds with uv |
| [`07-output.txt`](snippets/07-output.txt) | Output | text | 6. Running in Production: Gunicorn + Uvicorn Workers, Non-Root User |
| [`08-output.txt`](snippets/08-output.txt) | Output | text | 6. Running in Production: Gunicorn + Uvicorn Workers, Non-Root User |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 6. Running in Production: Gunicorn + Uvicorn Workers, Non-Root User |
| [`10-output.txt`](snippets/10-output.txt) | Output | text | 7. Sizing Workers to Container CPU and Memory |
| [`11-output.txt`](snippets/11-output.txt) | Output | text | 7. Sizing Workers to Container CPU and Memory |
| [`12-output.txt`](snippets/12-output.txt) | Output | text | 7. Sizing Workers to Container CPU and Memory |
| [`13-listing-19-4-compose-yaml.yml`](snippets/13-listing-19-4-compose-yaml.yml) | Listing 19-4: compose.yaml | yaml | 8. Docker Compose: App, PostgreSQL, Redis, Celery Worker |
| [`14-output.txt`](snippets/14-output.txt) | Output | text | 8. Docker Compose: App, PostgreSQL, Redis, Celery Worker |
| [`15-prompt.txt`](snippets/15-prompt.txt) | Prompt | prompt | 10. Writing Manifests with Claude Code and a Local Cluster (kind or minikube) |
| [`16-output.txt`](snippets/16-output.txt) | Output | text | 10. Writing Manifests with Claude Code and a Local Cluster (kind or minikube) |
| [`17-listing-19-5-k8s-deployment-yaml.yml`](snippets/17-listing-19-5-k8s-deployment-yaml.yml) | Listing 19-5: k8s/deployment.yaml | yaml | 10. Writing Manifests with Claude Code and a Local Cluster (kind or minikube) |
| [`18-listing-19-6-the-probe-endpoints-in-src-catalog-app-py.py`](snippets/18-listing-19-6-the-probe-endpoints-in-src-catalog-app-py.py) | Listing 19-6: The probe endpoints in src/catalog/app.py | python | 11. Health Probes, Graceful Shutdown, and Migrations as Jobs |
| [`19-output.txt`](snippets/19-output.txt) | Output | text | 11. Health Probes, Graceful Shutdown, and Migrations as Jobs |
| [`20-listing-19-7-k8s-migrate-job-yaml.yml`](snippets/20-listing-19-7-k8s-migrate-job-yaml.yml) | Listing 19-7: k8s/migrate-job.yaml | yaml | 11. Health Probes, Graceful Shutdown, and Migrations as Jobs |
| [`21-listing-19-8-chart-catalog-values-yaml.yml`](snippets/21-listing-19-8-chart-catalog-values-yaml.yml) | Listing 19-8: chart/catalog/values.yaml | yaml | 12. Helm: Packaging Everything into One Chart |
| [`22-listing-19-9-excerpt-from-chart-catalog-templates-deployme.yml`](snippets/22-listing-19-9-excerpt-from-chart-catalog-templates-deployme.yml) | Listing 19-9: Excerpt from chart/catalog/templates/deployment.yaml | yaml | 12. Helm: Packaging Everything into One Chart |
| [`23-output.txt`](snippets/23-output.txt) | Output | text | 12. Helm: Packaging Everything into One Chart |
| [`24-terminal.sh`](snippets/24-terminal.sh) | Terminal | bash | 13. End-to-End: From Dockerfile to a Running Helm Release |
| [`25-output.txt`](snippets/25-output.txt) | Output | text | 14. Troubleshooting the Errors Beginners Hit |
