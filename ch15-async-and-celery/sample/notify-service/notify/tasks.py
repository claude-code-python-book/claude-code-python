"""Celery tasks: thin wrappers around notify.pipeline."""

import os
from typing import Any

import redis
from celery import Celery, Task
from celery.utils.log import get_task_logger

from notify import delivery
from notify.clients import HttpServices
from notify.pipeline import deliver_confirmation

app = Celery("notify")
app.config_from_object("notify.celeryconfig")
logger = get_task_logger(__name__)

store = redis.Redis.from_url(
    os.environ.get("NOTIFY_REDIS_URL", "redis://localhost:6379/1")
)
send = delivery.smtp_sender(
    os.environ.get("SMTP_HOST", "localhost"), int(os.environ.get("SMTP_PORT", "25"))
)


class DeadLetterTask(Task):  # type: ignore[misc]
    """A task that records itself as a dead letter when it fails for good."""

    def on_failure(
        self, exc: Exception, task_id: str, args: Any, kwargs: Any, einfo: Any
    ) -> None:
        """Called by the worker once retries are used up, or on a permanent error."""
        order_id = kwargs.get("order_id", args[0] if args else None)
        delivery.record_dead_letter(store, order_id, f"{type(exc).__name__}: {exc}")
        logger.error("Confirmation for order %s failed for good: %s", order_id, exc)


@app.task(
    base=DeadLetterTask,
    autoretry_for=(delivery.TransientEmailError,),
    retry_backoff=True,  # 1 s, 2 s, 4 s, ... before jitter
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=6,
)
def send_order_confirmation(order_id: int) -> bool:
    """Send one order's confirmation email (at most once)."""
    return deliver_confirmation(order_id, HttpServices.from_env(), store, send)


@app.task
def report_dead_letters() -> int:
    """Log how many emails are parked as dead letters (run daily by beat)."""
    count = int(store.llen(delivery.DEAD_LETTERS))
    if count:
        logger.warning("%d order confirmations need attention", count)
    return count
