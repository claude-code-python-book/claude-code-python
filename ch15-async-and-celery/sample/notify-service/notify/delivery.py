"""Send an email at most once per key, and say whether a failure is worth retrying.

A job queue delivers a task at least once. With late acknowledgement, a task
can run twice: after a worker crash, or when a retry overlaps a slow first
attempt. The claim below makes the second run skip the email.
"""

import json
import smtplib
from collections.abc import Callable
from datetime import UTC, datetime
from email.message import EmailMessage
from typing import Protocol

CLAIM_SECONDS = 10 * 60  # longer than one attempt can take
SENT_SECONDS = 30 * 24 * 3600  # how long to remember a sent email
DEAD_LETTERS = "dead:order-confirmation"


class TransientEmailError(Exception):
    """Worth retrying later: the server is busy, down or unreachable."""


class PermanentEmailError(Exception):
    """Retrying won't help: for example, the address doesn't exist."""


class KeyStore(Protocol):
    """The two Redis commands we use, with redis-py's signatures."""

    def set(  # noqa: D102
        self, name: str, value: str, ex: int | None = None, nx: bool = False
    ) -> bool | None: ...

    def get(self, name: str) -> bytes | None: ...  # noqa: D102

    def delete(self, *names: str) -> int: ...  # noqa: D102

    def lpush(self, name: str, *values: str) -> int: ...  # noqa: D102


def classify(error: Exception) -> Exception:
    """Map an SMTP or network error to Transient or Permanent."""
    if isinstance(error, smtplib.SMTPRecipientsRefused):
        codes = [code for code, _ in error.recipients.values()]
        permanent = all(500 <= code < 600 for code in codes)
        kind = PermanentEmailError if permanent else TransientEmailError
        return kind(f"recipients refused: {codes}")
    if isinstance(error, smtplib.SMTPResponseException):
        kind = PermanentEmailError if error.smtp_code >= 500 else TransientEmailError
        return kind(f"SMTP {error.smtp_code}: {error.smtp_error!r}")
    if isinstance(error, (smtplib.SMTPServerDisconnected, OSError)):
        return TransientEmailError(f"{type(error).__name__}: {error}")
    return error


def send_once(
    store: KeyStore,
    key: str,
    message: EmailMessage,
    send: Callable[[EmailMessage], object],
) -> bool:
    """Send `message` unless it was already sent under `key`.

    Returns True if this call sent it, False if it had been sent before.

    Raises:
        TransientEmailError: If sending failed but may work later, or
            another worker is sending the same email right now.
        PermanentEmailError: If sending failed for good.
    """
    if not store.set(key, "sending", ex=CLAIM_SECONDS, nx=True):
        if store.get(key) == b"sent":
            return False
        raise TransientEmailError(f"{key} is being sent by another worker")
    try:
        send(message)
    except Exception as error:
        store.delete(key)  # let the next attempt claim it
        mapped = classify(error)
        if mapped is error:
            raise
        raise mapped from error
    store.set(key, "sent", ex=SENT_SECONDS)
    return True


def smtp_sender(
    host: str, port: int, timeout: float = 10
) -> Callable[[EmailMessage], object]:
    """Return a function that sends one message through an SMTP server."""

    def send(message: EmailMessage) -> object:
        with smtplib.SMTP(host, port, timeout=timeout) as smtp:
            return smtp.send_message(message)

    return send


def record_dead_letter(store: KeyStore, order_id: int, reason: str) -> None:
    """Park an email that will never be sent, so a person can look at it."""
    entry = {
        "order_id": order_id,
        "reason": reason,
        "at": datetime.now(UTC).isoformat(),
    }
    store.lpush(DEAD_LETTERS, json.dumps(entry))
