# Chapter 15 — Async Python and Background Jobs: asyncio and Celery

Code and snippets exactly as they appear in the chapter, in reading order.

> **Reference material, not production-ready code.** Verify every snippet against the official documentation for the tools involved, and test it in your own environment, before you use it in your codebase. See the notice in the [repository README](../README.md).

## Sample project

`sample/` is the tested sample project for this chapter (`notify-service`). See the README inside it for how to run it.

## Snippets

| File | What it is | Type | Section |
| --- | --- | --- | --- |
| [`01-output.txt`](snippets/01-output.txt) | Output | text | 1. Concurrency in Python: Threads, Processes, asyncio, and the GIL |
| [`02-listing-15-1-the-async-and-task-rules-in-claude-md.md`](snippets/02-listing-15-1-the-async-and-task-rules-in-claude-md.md) | Listing 15-1: The async and task rules in CLAUDE.md | markdown | 2. Writing Correct async Code with Claude Code |
| [`03-code.py`](snippets/03-code.py) | Code | python | 2. Writing Correct async Code with Claude Code |
| [`04-output.txt`](snippets/04-output.txt) | Output | text | 2. Writing Correct async Code with Claude Code |
| [`05-output.txt`](snippets/05-output.txt) | Output | text | 3. Finding Blocking Calls Hidden in async Paths |
| [`06-code.py`](snippets/06-code.py) | Code | python | 3. Finding Blocking Calls Hidden in async Paths |
| [`07-output.txt`](snippets/07-output.txt) | Output | text | 3. Finding Blocking Calls Hidden in async Paths |
| [`08-code.py`](snippets/08-code.py) | Code | python | 3. Finding Blocking Calls Hidden in async Paths |
| [`09-output.txt`](snippets/09-output.txt) | Output | text | 3. Finding Blocking Calls Hidden in async Paths |
| [`10-prompt.txt`](snippets/10-prompt.txt) | Prompt | prompt | 3. Finding Blocking Calls Hidden in async Paths |
| [`11-listing-15-2-optional-and-order-summary-in-notify-summary.py`](snippets/11-listing-15-2-optional-and-order-summary-in-notify-summary.py) | Listing 15-2: optional() and order_summary() in notify/summary.py | python | 4. TaskGroups, Timeouts, and Cancellation |
| [`12-listing-15-3-two-tests-from-tests-test-summary-py.py`](snippets/12-listing-15-3-two-tests-from-tests-test-summary-py.py) | Listing 15-3: Two tests from tests/test_summary.py | python | 4. TaskGroups, Timeouts, and Cancellation |
| [`13-code.py`](snippets/13-code.py) | Code | python | 4. TaskGroups, Timeouts, and Cancellation |
| [`14-output.txt`](snippets/14-output.txt) | Output | text | 4. TaskGroups, Timeouts, and Cancellation |
| [`15-listing-15-4-notify-celeryconfig-py.py`](snippets/15-listing-15-4-notify-celeryconfig-py.py) | Listing 15-4: notify/celeryconfig.py | python | 5. Background Jobs with Celery and Redis |
| [`16-listing-15-5-send-once-in-notify-delivery-py.py`](snippets/16-listing-15-5-send-once-in-notify-delivery-py.py) | Listing 15-5: send_once() in notify/delivery.py | python | 6. Retries, Idempotency, and Dead Tasks |
| [`17-output.txt`](snippets/17-output.txt) | Output | text | 6. Retries, Idempotency, and Dead Tasks |
| [`18-listing-15-6-the-task-in-notify-tasks-py.py`](snippets/18-listing-15-6-the-task-in-notify-tasks-py.py) | Listing 15-6: The task in notify/tasks.py | python | 6. Retries, Idempotency, and Dead Tasks |
| [`19-output.txt`](snippets/19-output.txt) | Output | text | 8. Lighter Options: FastAPI BackgroundTasks, RQ, Dramatiq |
| [`20-listing-15-7-deliver-confirmation-in-notify-pipeline-py.py`](snippets/20-listing-15-7-deliver-confirmation-in-notify-pipeline-py.py) | Listing 15-7: deliver_confirmation() in notify/pipeline.py | python | 9. Testing async Code and Celery Tasks |
| [`21-output.txt`](snippets/21-output.txt) | Output | text | 9. Testing async Code and Celery Tasks |
| [`22-code.py`](snippets/22-code.py) | Code | python | 9. Testing async Code and Celery Tasks |
