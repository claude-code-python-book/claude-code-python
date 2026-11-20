"""Payment reminders for overdue invoices."""

import asyncio
import logging
import os
import sqlite3
from collections.abc import (
    Callable,
    Collection,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
)
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


def iter_due(
    invoices: Iterable[Mapping[str, str]], already_sent: Collection[str] = ()
) -> Iterator[str]:
    """Yield the ids of overdue invoices that have not had a reminder yet.

    This is a generator: it reads `invoices` one at a time, as the caller asks
    for ids, so it works on a stream of rows too large to hold in memory.

    Args:
        invoices: Mappings with at least `"id"` and `"status"` keys.
        already_sent: Ids that were reminded before. They are skipped.

    Yields:
        Each due invoice id, in the order of `invoices`.

    Raises:
        KeyError: If an invoice has no `"id"` or `"status"`. Like any error in
            a generator, it is raised during iteration, not when `iter_due`
            is called.
    """
    for invoice in invoices:
        if invoice["status"] == "overdue" and invoice["id"] not in already_sent:
            yield invoice["id"]


def due_reminders(
    invoices: Iterable[Mapping[str, str]], already_sent: Collection[str] = ()
) -> list[str]:
    """Return the ids of overdue invoices that have not had a reminder yet.

    The list form of `iter_due`; see there for the arguments.
    """
    return list(iter_due(invoices, already_sent))


def reminder_text(invoice_id: str) -> str:
    """Return the reminder message for one invoice."""
    return f"remind {invoice_id}"


def schedule(invoice_ids: Iterable[str]) -> list[Callable[[], str]]:
    """One job per invoice; the scheduler calls each job later."""
    return [partial(reminder_text, invoice_id) for invoice_id in invoice_ids]


def find_customer(db: sqlite3.Connection, name: str) -> tuple[int, str] | None:
    """Return the `(id, email)` of the customer called `name`, or None."""
    row: tuple[int, str] | None = db.execute(
        "SELECT id, email FROM customers WHERE name = ?", (name,)
    ).fetchone()
    return row


def reminder_emails(
    db: sqlite3.Connection, invoice_ids: Sequence[str]
) -> dict[str, str]:
    """Return the customer email for each invoice id, with one query.

    Args:
        db: A connection with `invoices` and `customers` tables.
        invoice_ids: The invoices to look up. Duplicates are allowed.

    Returns:
        A dict from invoice id to email. An id with no matching invoice or
        customer is left out, so compare the keys with `invoice_ids` to find
        the missing ones.
    """
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
    """Return the customer's email, stripped and lower-cased.

    Raises:
        ValueError: If `contacts` has no entry for `customer`.
    """
    email = contacts.get(customer)
    if email is None:
        raise ValueError(f"no contact email for {customer!r}")
    return email.strip().lower()


def load_sent(path: Path) -> list[str]:
    """Read the ids already reminded, stored as a JSON list of strings.

    Raises:
        pydantic.ValidationError: If the file holds anything else.
    """
    return SENT_IDS.validate_json(path.read_bytes())


def post(message: str, token: str) -> None:
    """Send one message to the reminders webhook. This call blocks.

    Raises:
        urllib.error.URLError: If the webhook can't be reached or answers
            with an HTTP error status.
    """
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
