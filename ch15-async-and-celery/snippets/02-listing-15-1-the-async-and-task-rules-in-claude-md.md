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
