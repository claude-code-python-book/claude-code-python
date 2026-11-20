"""Celery app, the alert task, and the queue adapter the service uses."""

from __future__ import annotations

import logging

from celery import Celery

from . import settings

log = logging.getLogger(__name__)
celery_app = Celery("bookshop", broker=settings.REDIS_URL)


@celery_app.task(autoretry_for=(OSError,), retry_backoff=True,
                 retry_kwargs={"max_retries": 5})
def low_rating_alert(book_id: int) -> None:
    # Receives an ID, not an object: the worker reads committed data itself.
    log.warning("book %s fell below the rating alert threshold", book_id)


class CeleryQueue:
    def low_rating_alert(self, book_id: int) -> None:
        low_rating_alert.delay(book_id)
