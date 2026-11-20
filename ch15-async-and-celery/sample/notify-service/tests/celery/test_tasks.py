"""Tests for the Celery wrappers. They need celery, redis and httpx installed.

Following the Celery testing guide, these mock what the task calls instead
of running it in eager mode.
"""

from unittest.mock import patch

import pytest

pytest.importorskip("celery")
pytest.importorskip("httpx")

from notify import tasks
from notify.delivery import PermanentEmailError, TransientEmailError


def test_the_task_only_calls_the_pipeline() -> None:
    with (
        patch.object(tasks, "deliver_confirmation", return_value=True) as deliver,
        patch.object(tasks.HttpServices, "from_env") as services,
    ):
        assert tasks.send_order_confirmation.run(1042) is True
    deliver.assert_called_once_with(
        1042, services.return_value, tasks.store, tasks.send
    )


def test_only_transient_errors_are_retried() -> None:
    task = tasks.send_order_confirmation
    assert task.autoretry_for == (TransientEmailError,)
    assert (task.retry_backoff, task.retry_backoff_max, task.retry_jitter) == (
        True,
        600,
        True,
    )
    assert task.max_retries == 6


def test_a_final_failure_becomes_a_dead_letter() -> None:
    with patch.object(tasks.delivery, "record_dead_letter") as record:
        tasks.send_order_confirmation.on_failure(
            PermanentEmailError("order 999 not found"), "task-id", (999,), {}, None
        )
    record.assert_called_once_with(
        tasks.store, 999, "PermanentEmailError: order 999 not found"
    )
