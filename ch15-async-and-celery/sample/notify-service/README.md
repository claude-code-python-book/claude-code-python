# notify-service

Sample project for Chapter 15 of *Claude Code for Python Developers*: order
confirmation emails, gathered with asyncio and sent by Celery workers.

```bash
uv sync
redis-server &                         # or: docker run -p 6379:6379 redis
uv run pytest                          # plain-Python tests need only Redis
uv run celery -A notify.tasks worker --loglevel=info
uv run celery -A notify.tasks beat     # one instance only
```

`tests/celery` needs Celery, redis-py and httpx installed, which `uv sync` does.
