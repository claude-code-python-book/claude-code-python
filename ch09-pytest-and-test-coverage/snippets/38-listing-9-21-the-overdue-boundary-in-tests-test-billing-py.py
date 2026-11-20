@pytest.mark.parametrize(
    ("issued", "status"),
    [("2026-10-16", "open"), ("2026-10-15", "overdue")],
    ids=["30-days-old", "31-days-old"],
)
def test_invoice_becomes_overdue_after_30_days(
    make_row: RowFactory, issued: str, status: str
) -> None:
    result = summarize_billing([make_row(issued=issued)], TODAY)
    assert result["invoices"]["INV-1"]["status"] == status
