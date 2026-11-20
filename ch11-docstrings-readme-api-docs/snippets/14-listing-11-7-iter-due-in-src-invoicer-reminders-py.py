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
