# notify-service

Sends order confirmation emails in the background. Python 3.12+, asyncio for
I/O fan-out, Celery 5.7 with a Redis broker for the jobs.

## Commands

- Tests: `uv run pytest` (needs Redis on localhost:6379; uses database 15)
- Lint and types: `uv run ruff check . && uv run ruff format --check . && uv run mypy notify`
- Worker: `uv run celery -A notify.tasks worker --loglevel=info`
- Scheduler: `uv run celery -A notify.tasks beat` (exactly one, ever)

## Where things go

- Async fan-out to other services: `notify/summary.py`
- The email: `notify/emails.py`. Sending, idempotency, errors: `notify/delivery.py`
- One job end to end, no Celery: `notify/pipeline.py`
- Celery app, tasks and settings: `notify/tasks.py`, `notify/celeryconfig.py`

## Async rules

- No blocking calls in `async def`: no `time.sleep`, `requests`, `open()`,
  `subprocess.run`, or sync database drivers. Use the async library, or
  `await asyncio.to_thread(...)` for code that has no async version.
- Run concurrent work in an `asyncio.TaskGroup`, never bare `create_task()`
  without keeping a reference.
- Put a time limit on every network call: `async with asyncio.timeout(...)`.
- Never swallow `asyncio.CancelledError`. Catch `Exception`, not
  `BaseException`, and re-raise cancellation after cleanup.
- Ruff's `ASYNC` rules are on; fix what they report, don't silence it.

## Task rules

- Tasks are thin: parse arguments, call `notify.pipeline`, return.
- Pass IDs to tasks, never objects. Enqueue only after the database commit.
- Every task must be safe to run twice (`acks_late` is on). Side effects go
  through `send_once()` or another idempotency key.
- Retry only `TransientEmailError`, with backoff and jitter. Anything
  permanent fails at once and lands in the dead-letter list.
- Keep every retry delay under the broker's visibility timeout (1 hour).
- Never start a second `celery beat`, and never run `celery purge`.

## Testing

- Business logic: plain pytest, no broker. Async tests use `@pytest.mark.anyio`.
- Delivery tests use the real local Redis and the fake SMTP server in `tests/`.
- Celery wrappers: mock what the task calls; don't use `task_always_eager`.
