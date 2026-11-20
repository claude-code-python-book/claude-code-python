import pytest

from notify.delivery import PermanentEmailError, smtp_sender
from notify.pipeline import deliver_confirmation, idempotency_key
from tests.conftest import ORDER, FakeServices
from tests.resp import MiniRedis
from tests.smtp_server import smtp_server


def test_an_order_gets_one_confirmation(redis: MiniRedis) -> None:
    services = FakeServices(delay=0.01)
    with smtp_server() as (port, box):
        send = smtp_sender("127.0.0.1", port)
        assert deliver_confirmation(ORDER.id, services, redis, send) is True
        assert deliver_confirmation(ORDER.id, services, redis, send) is False
    assert len(box.messages) == 1
    received = box.messages[0].decode()
    assert "Subject: Your order #1042 is confirmed" in received
    assert "Expected delivery: Thursday 19 November." in received
    assert redis.get(idempotency_key(ORDER.id)) == b"sent"


def test_a_missing_order_is_permanent(redis: MiniRedis) -> None:
    with pytest.raises(PermanentEmailError, match="order 999 not found"):
        deliver_confirmation(999, FakeServices(delay=0.01), redis, lambda m: None)
