from invoicer.reminders import due_reminders


def test_due_reminders_picks_overdue_invoices() -> None:
    invoices = [
        {"id": "INV-1", "status": "overdue"},
        {"id": "INV-2", "status": "paid"},
    ]
    assert due_reminders(invoices) == ["INV-1"]
