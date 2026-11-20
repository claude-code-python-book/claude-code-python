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
