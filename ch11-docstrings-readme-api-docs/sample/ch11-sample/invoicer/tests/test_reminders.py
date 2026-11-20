import asyncio
import sqlite3
from collections.abc import Iterator
from pathlib import Path
from urllib.error import URLError

import pytest
from pydantic import ValidationError

from invoicer import reminders

INVOICES = [
    {"id": "INV-1", "status": "overdue"},
    {"id": "INV-2", "status": "paid"},
    {"id": "INV-3", "status": "overdue"},
]


@pytest.fixture
def db() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
        CREATE TABLE invoices (id TEXT PRIMARY KEY, customer_id INTEGER);
        INSERT INTO customers VALUES (1, 'Acme Ltd', 'ap@acme.test');
        INSERT INTO customers VALUES (2, 'Globex', 'billing@globex.test');
        INSERT INTO invoices VALUES ('INV-1', 1), ('INV-2', 2), ('INV-3', 1);
        """
    )
    yield conn
    conn.close()


def test_due_reminders_skips_paid_and_already_sent() -> None:
    assert reminders.due_reminders(INVOICES, already_sent={"INV-1"}) == ["INV-3"]


def test_due_reminders_keeps_no_state_between_calls() -> None:
    assert reminders.due_reminders(INVOICES) == ["INV-1", "INV-3"]
    assert reminders.due_reminders(INVOICES[1:]) == ["INV-3"]


def test_each_scheduled_job_remembers_its_own_invoice() -> None:
    jobs = reminders.schedule(["INV-1", "INV-3"])
    assert [job() for job in jobs] == ["remind INV-1", "remind INV-3"]


def test_find_customer_treats_the_name_as_data(db: sqlite3.Connection) -> None:
    assert reminders.find_customer(db, "Acme Ltd") == (1, "ap@acme.test")
    assert reminders.find_customer(db, "x' OR '1'='1") is None


def test_reminder_emails_uses_one_query(db: sqlite3.Connection) -> None:
    statements: list[str] = []
    db.set_trace_callback(statements.append)
    emails = reminders.reminder_emails(db, ["INV-1", "INV-3", "INV-9"])
    assert emails == {"INV-1": "ap@acme.test", "INV-3": "ap@acme.test"}
    assert len(statements) == 1


def test_contact_for_reports_a_missing_customer() -> None:
    with pytest.raises(ValueError, match="no contact email for 'Initech'"):
        reminders.contact_for({"Acme Ltd": "ap@acme.test"}, "Initech")


def test_load_sent_reads_json_and_rejects_anything_else(tmp_path: Path) -> None:
    good, bad = tmp_path / "sent.json", tmp_path / "bad.json"
    good.write_text('["INV-1", "INV-3"]')
    bad.write_text('{"INV-1": true}')
    assert reminders.load_sent(good) == ["INV-1", "INV-3"]
    with pytest.raises(ValidationError):
        reminders.load_sent(bad)


def test_post_all_reports_failures_and_keeps_going(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(message: str, token: str) -> None:
        if message == "remind INV-3":
            raise URLError("timed out")

    monkeypatch.setattr(reminders, "post", fake_post)
    messages = ["remind INV-1", "remind INV-3"]
    failed = asyncio.run(reminders.post_all(messages, "test-token", delay=0))
    assert failed == ["remind INV-3"]


def test_iter_due_is_lazy_and_fails_on_iteration() -> None:
    due = reminders.iter_due([{"id": "INV-1"}])  # no error yet: nothing read
    with pytest.raises(KeyError, match="status"):
        next(due)


def test_iter_due_yields_in_order() -> None:
    assert list(reminders.iter_due(INVOICES)) == ["INV-1", "INV-3"]
