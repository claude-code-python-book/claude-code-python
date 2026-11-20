"""Celery worker for background jobs (Chapter 15 covers Celery in depth).

Start it with: celery -A catalog.tasks worker --loglevel=INFO
"""

import os

from celery import Celery

celery_app = Celery(
    "catalog", broker=os.environ.get("REDIS_URL", "redis://localhost:6379/0")
)


@celery_app.task
def reindex_product(product_id: int) -> str:
    return f"reindexed {product_id}"
