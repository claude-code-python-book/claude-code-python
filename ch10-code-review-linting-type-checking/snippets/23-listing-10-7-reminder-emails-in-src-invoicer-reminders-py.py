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
