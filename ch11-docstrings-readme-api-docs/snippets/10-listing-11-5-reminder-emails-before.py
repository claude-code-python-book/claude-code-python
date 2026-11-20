def reminder_emails(
    db: sqlite3.Connection, invoice_ids: Sequence[str]
) -> dict[str, str]:
    """Map each invoice id to its customer's email, with one query."""
