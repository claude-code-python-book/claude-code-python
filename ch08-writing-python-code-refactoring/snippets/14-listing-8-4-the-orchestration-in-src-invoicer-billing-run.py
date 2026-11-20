def run_billing(rows, today, report_dir=None):
    invoices, errors = collect_invoices(rows)
    bills = {
        inv_id: bill_invoice(invoices[inv_id], today) for inv_id in sorted(invoices)
    }
    customers = summarize_customers(bills)
    if report_dir is not None:
        write_report(customers, report_dir)
    grand = sum(
        (Decimal(b["gross"]) + Decimal(b["fee"]) for b in bills.values()), Decimal("0")
    )
    return {
        "invoices": bills,
        "customers": customers,
        "errors": errors,
        "grand_total": str(grand),
    }


def collect_invoices(rows):
    invoices = {}
    errors = []
    for n, row in enumerate(rows, start=2):  # row 1 is the CSV header
        try:
            line = parse_row(row)
            add_line(invoices, line)
        except RowError as exc:
            errors.append(f"row {n}: {exc}")
    return invoices, errors
