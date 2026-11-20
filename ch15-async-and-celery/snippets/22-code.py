def test_only_transient_errors_are_retried() -> None:
    task = tasks.send_order_confirmation
    assert task.autoretry_for == (TransientEmailError,)
    assert (task.retry_backoff, task.retry_backoff_max, task.retry_jitter) == (
        True,
        600,
        True,
    )
    assert task.max_retries == 6
