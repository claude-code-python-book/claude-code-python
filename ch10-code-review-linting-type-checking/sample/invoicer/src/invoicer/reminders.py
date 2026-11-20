"""Payment reminders for overdue invoices."""

import asyncio
import logging
import os
import sqlite3
from collections.abc import Callable, Collection, Iterable, Mapping, Sequence
from functools import partial
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from pydantic import TypeAdapter

log = logging.getLogger(__name__)

WEBHOOK_URL = "https://hooks.example.com/reminders"
SENT_IDS = TypeAdapter(list[str])


def webhook_token() -> str:
    """The webhook's bearer token, from the environment, never from the code."""
    return os.environ["INVOICER_WEBHOOK_TOKEN"]


def due_reminders(
    invoices: Iterable[Mapping[str, str]], already_sent: Collection[str] = ()
) -> list[str]:
    """Return the ids of overdue invoices that have not had a reminder yet."""
    return [
        invoice["id"]
        for invoice in invoices
        if invoice["status"] == "overdue" and invoice["id"] not in already_sent
    ]


def reminder_text(invoice_id: str) -> str:
    return f"remind {invoice_id}"


def schedule(invoice_ids: Iterable[str]) -> list[Callable[[], str]]:
    """One job per invoice; the scheduler calls each job later."""
    return [partial(reminder_text, invoice_id) for invoice_id in invoice_ids]


def find_customer(db: sqlite3.Connection, name: str) -> tuple[int, str] | None:
    row: tuple[int, str] | None = db.execute(
        "SELECT id, email FROM customers WHERE name = ?", (name,)
    ).fetchone()
    return row


def reminder_emails(
    db: sqlite3.Connection, invoice_ids: Sequence[str]
) -> dict[str, str]:
    """Map each invoice id to its customer's email, with one query."""
    if not invoice_ids:
        return {}
    placeholders = ", ".join("?" * len(invoice_ids))
    # Only "?" placeholders are formatted into the SQL; the values are bound.
    query = f"""
        SELECT i.id, c.email
        FROM invoices i JOIN customers c ON c.id = i.customer_id
        WHERE i.id IN ({placeholders})
    """  # noqa: S608
    rows: list[tuple[str, str]] = db.execute(query, list(invoice_ids)).fetchall()
    return dict(rows)


def contact_for(contacts: Mapping[str, str], customer: str) -> str:
    email = contacts.get(customer)
    if email is None:
        raise ValueError(f"no contact email for {customer!r}")
    return email.strip().lower()


def load_sent(path: Path) -> list[str]:
    """Read the ids already reminded, stored as a JSON list of strings."""
    return SENT_IDS.validate_json(path.read_bytes())


def post(message: str, token: str) -> None:
    request = Request(
        WEBHOOK_URL,
        data=message.encode(),
        headers={"Authorization": f"Bearer {token}"},
    )
    # WEBHOOK_URL is a fixed https URL, so urlopen can't be sent to file: URLs.
    with urlopen(request, timeout=5):  # noqa: S310
        pass


async def post_all(
    messages: Iterable[str], token: str, delay: float = 1.0
) -> list[str]:
    """Post each message, at most one per `delay` seconds; return the failures."""
    failed: list[str] = []
    for message in messages:
        try:
            await asyncio.to_thread(post, message, token)
        except URLError as error:
            log.warning("reminder not sent: %s", error)
            failed.append(message)
        await asyncio.sleep(delay)
    return failed
