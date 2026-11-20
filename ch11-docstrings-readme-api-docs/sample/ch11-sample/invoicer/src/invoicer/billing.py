"""Monthly billing run: validate export rows, bill invoices, total customers."""

import csv
import os
from collections.abc import Iterable, Mapping
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import TypedDict

from pydantic import ValidationError

from invoicer.billing_models import Bill, BillingRow, CustomerTotals, Invoice, Region

TAX: dict[Region, Decimal] = {
    "UK": Decimal("0.20"),
    "DE": Decimal("0.19"),
    "US-CA": Decimal("0.0725"),
    "IN": Decimal("0.18"),
}
CENT = Decimal("0.01")


class RowError(ValueError):
    """A row the billing run rejects. The message says why."""


class BillingResult(TypedDict):
    """What `summarize_billing` returns; every amount is a string such as "12.34"."""

    invoices: dict[str, dict[str, str | int]]
    customers: dict[str, dict[str, str | int]]
    errors: list[str]
    grand_total: str


def summarize_billing(
    rows: Iterable[Mapping[str, str]],
    today: date,
    report_dir: str | os.PathLike[str] | None = None,
) -> BillingResult:
    """Bill every invoice in `rows` as of `today`.

    Rows that fail validation are skipped and reported in `errors` by their
    line number in the CSV file. If `report_dir` is given, a per-customer
    summary is also written to `customers.csv` in that directory.
    """
    invoices, errors = collect_invoices(rows)
    bills = {
        inv_id: bill_invoice(invoices[inv_id], today) for inv_id in sorted(invoices)
    }
    customers = summarize_customers(bills)
    if report_dir is not None:
        write_report(customers, report_dir)
    grand = sum((b.gross + b.fee for b in bills.values()), Decimal(0))
    return {
        "invoices": {inv_id: bill.to_dict() for inv_id, bill in bills.items()},
        "customers": {name: t.to_dict() for name, t in customers.items()},
        "errors": errors,
        "grand_total": str(grand),
    }


def collect_invoices(
    rows: Iterable[Mapping[str, str]],
) -> tuple[dict[str, Invoice], list[str]]:
    """Group valid rows into invoices and describe each invalid row.

    Returns:
        The invoices by id, and one error message per rejected row, such as
        `"row 3: qty: Input should be greater than 0"`. Row numbers count the
        CSV header as row 1.
    """
    invoices: dict[str, Invoice] = {}
    errors: list[str] = []
    for n, row in enumerate(rows, start=2):  # row 1 is the CSV header
        try:
            add_line(invoices, parse_row(row))
        except RowError as exc:
            errors.append(f"row {n}: {exc}")
    return invoices, errors


def parse_row(row: Mapping[str, str]) -> BillingRow:
    """Validate one CSV row.

    Raises:
        RowError: If the row is invalid. The message names the first bad field.
    """
    try:
        return BillingRow.model_validate(row)
    except ValidationError as exc:
        first = exc.errors()[0]
        where = ".".join(str(part) for part in first["loc"])
        raise RowError(f"{where}: {first['msg']}" if where else first["msg"]) from None


def line_net(row: BillingRow) -> Decimal:
    """Return the line total before tax, after any discount.

    `SAVE10` takes 10% off any line. `BULK5` takes 5% off, but only when the
    quantity is 100 or more. The result is not rounded.
    """
    net = row.unit_price * row.qty
    if row.discount == "SAVE10":
        net = net - net * Decimal("0.10")
    elif row.discount == "BULK5" and row.qty >= 100:
        net = net - net * Decimal("0.05")
    return net


def add_line(invoices: dict[str, Invoice], row: BillingRow) -> None:
    """Add a row to its invoice in `invoices`, creating the invoice if needed.

    Raises:
        RowError: If the row names a different customer or region than earlier
            rows of the same invoice.
    """
    inv = invoices.get(row.invoice_id)
    if inv is None:
        invoices[row.invoice_id] = Invoice(
            row.invoice_id,
            row.customer,
            row.region,
            row.issued,
            row.paid,
            line_net(row),
        )
        return
    if inv.customer != row.customer or inv.region != row.region:
        raise RowError(f"invoice {row.invoice_id} changes")
    inv.net += line_net(row)
    inv.lines += 1


def bill_invoice(inv: Invoice, today: date) -> Bill:
    """Bill one invoice as of `today`.

    Tax is added at the region's rate and rounded half-up to cents. A paid
    invoice owes no fee. An unpaid invoice more than 30 days old is overdue
    and owes `late_fee`; otherwise it is open.
    """
    gross = (inv.net + inv.net * TAX[inv.region]).quantize(CENT, rounding=ROUND_HALF_UP)
    days = (today - inv.issued).days
    if inv.paid is not None:
        return Bill(inv.customer, inv.lines, gross, Decimal("0.00"), "paid")
    if days > 30:
        return Bill(inv.customer, inv.lines, gross, late_fee(gross, days), "overdue")
    return Bill(inv.customer, inv.lines, gross, Decimal("0.00"), "open")


def late_fee(gross: Decimal, days: int) -> Decimal:
    """Return the late fee on an overdue invoice.

    The fee is 1.5% of `gross` per period, capped at 10% of `gross`, rounded
    half-up to cents. Days 31 to 59 count as one period, days 60 to 89 as two,
    and so on: a new period starts every 30 days from day 60. Whether day 60
    should still be one period is an open question; see
    `docs/adr/0003-late-fee-periods.md`.

    Args:
        gross: The invoice total including tax.
        days: Days since the invoice was issued. Callers pass more than 30.

    Examples:
        >>> late_fee(Decimal("100.00"), 31)
        Decimal('1.50')
        >>> late_fee(Decimal("100.00"), 60)
        Decimal('3.00')
        >>> late_fee(Decimal("100.00"), 3650)
        Decimal('10.00')
    """
    periods = (days - 30) // 30 + 1
    fee = min(gross * Decimal("0.015") * periods, gross * Decimal("0.10"))
    return fee.quantize(CENT, rounding=ROUND_HALF_UP)


def summarize_customers(bills: Mapping[str, Bill]) -> dict[str, CustomerTotals]:
    """Total the bills per customer."""
    customers: dict[str, CustomerTotals] = {}
    for bill in bills.values():
        customers.setdefault(bill.customer, CustomerTotals()).add(bill)
    return customers


def write_report(
    customers: Mapping[str, CustomerTotals], report_dir: str | os.PathLike[str]
) -> None:
    """Write `customers.csv` to `report_dir`, one row per customer, sorted by name.

    The directory must exist. An existing `customers.csv` is replaced.
    """
    path = Path(report_dir) / "customers.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["customer", "invoices", "billed", "fees", "outstanding"])
        writer.writerows(
            [name, t.invoices, t.billed, t.fees, t.outstanding]
            for name, t in sorted(customers.items())
        )
