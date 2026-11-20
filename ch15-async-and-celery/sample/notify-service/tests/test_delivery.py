import json
import smtplib
from email.message import EmailMessage

import pytest

from notify.delivery import (
    DEAD_LETTERS,
    PermanentEmailError,
    TransientEmailError,
    classify,
    record_dead_letter,
    send_once,
    smtp_sender,
)
from tests.resp import MiniRedis
from tests.smtp_server import smtp_server

KEY = "email:order-confirmation:1042"


def message() -> EmailMessage:
    msg = EmailMessage()
    msg["From"], msg["To"], msg["Subject"] = "a@shop.example", "b@example.com", "Hi"
    msg.set_content("Hello")
    return msg


def test_the_email_is_sent_once(redis: MiniRedis) -> None:
    with smtp_server() as (port, box):
        send = smtp_sender("127.0.0.1", port)
        assert send_once(redis, KEY, message(), send) is True
        assert send_once(redis, KEY, message(), send) is False  # the retry
    assert len(box.messages) == 1
    assert redis.get(KEY) == b"sent"
    assert redis.ttl(KEY) > 29 * 24 * 3600


def test_a_concurrent_attempt_is_retried_later(redis: MiniRedis) -> None:
    redis.set(KEY, "sending", ex=600, nx=True)  # another worker holds the claim
    with pytest.raises(TransientEmailError, match="another worker"):
        send_once(redis, KEY, message(), lambda m: None)


def test_a_busy_server_is_transient_and_releases_the_claim(redis: MiniRedis) -> None:
    with smtp_server() as (port, box):
        box.fail_at = "MAIL"
        with pytest.raises(TransientEmailError, match="421"):
            send_once(redis, KEY, message(), smtp_sender("127.0.0.1", port))
        assert redis.get(KEY) is None
        box.fail_at = None  # the server recovers; the retry goes through
        assert send_once(redis, KEY, message(), smtp_sender("127.0.0.1", port))
    assert len(box.messages) == 1


def test_an_unknown_address_is_permanent(redis: MiniRedis) -> None:
    with smtp_server() as (port, box):
        box.fail_at, box.fail_reply = "RCPT", b"550 5.1.1 No such user"
        with pytest.raises(PermanentEmailError, match=r"\[550\]"):
            send_once(redis, KEY, message(), smtp_sender("127.0.0.1", port))


def test_no_server_at_all_is_transient(redis: MiniRedis) -> None:
    with smtp_server() as (port, _):
        pass  # the port is closed again
    with pytest.raises(TransientEmailError, match="ConnectionRefusedError"):
        send_once(redis, KEY, message(), smtp_sender("127.0.0.1", port, timeout=2))


def test_unknown_errors_are_not_disguised(redis: MiniRedis) -> None:
    def broken(m: EmailMessage) -> None:
        raise ValueError("bug in our code")

    with pytest.raises(ValueError, match="bug in our code"):
        send_once(redis, KEY, message(), broken)
    assert redis.get(KEY) is None


@pytest.mark.parametrize(
    ("error", "kind"),
    [
        (smtplib.SMTPResponseException(451, b"Local error"), TransientEmailError),
        (smtplib.SMTPResponseException(554, b"Rejected"), PermanentEmailError),
        (smtplib.SMTPServerDisconnected("gone"), TransientEmailError),
        (TimeoutError("timed out"), TransientEmailError),
        (smtplib.SMTPRecipientsRefused({"x@y": (450, b"busy")}), TransientEmailError),
    ],
)
def test_classify(error: Exception, kind: type[Exception]) -> None:
    assert isinstance(classify(error), kind)


def test_dead_letters_are_kept_newest_first(redis: MiniRedis) -> None:
    record_dead_letter(redis, 1041, "PermanentEmailError: recipients refused: [550]")
    record_dead_letter(redis, 1042, "TransientEmailError: SMTP 421")
    entries = [json.loads(e) for e in redis.lrange(DEAD_LETTERS, 0, -1)]
    assert [e["order_id"] for e in entries] == [1042, 1041]
