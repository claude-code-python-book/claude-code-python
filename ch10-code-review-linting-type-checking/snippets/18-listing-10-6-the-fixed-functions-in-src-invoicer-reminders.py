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
