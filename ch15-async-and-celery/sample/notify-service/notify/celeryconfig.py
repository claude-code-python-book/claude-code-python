"""Celery settings for the notify worker and beat."""

import os

from celery.schedules import crontab

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
task_ignore_result = True  # nothing reads task results; don't store them

# Acknowledge after the task finishes, and requeue it if the worker dies.
# Safe only because send_once() makes the task idempotent.
task_acks_late = True
task_reject_on_worker_lost = True
worker_prefetch_multiplier = 1  # long, slow tasks: don't hoard messages

# Redis redelivers unacknowledged messages after the visibility timeout.
# Keep it longer than any retry countdown (retry_backoff_max is 600 s).
broker_transport_options = {"visibility_timeout": 3600}

task_soft_time_limit = 60  # raises SoftTimeLimitExceeded in the task
task_time_limit = 90  # then the worker process is killed

timezone = "UTC"
beat_schedule = {
    "report-dead-letters": {
        "task": "notify.tasks.report_dead_letters",
        "schedule": crontab(hour=8, minute=5),
    },
}
