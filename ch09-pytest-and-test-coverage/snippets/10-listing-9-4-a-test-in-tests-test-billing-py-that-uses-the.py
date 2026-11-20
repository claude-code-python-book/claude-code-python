def test_paid_invoice_owes_no_late_fee(make_row: RowFactory) -> None:
    row = make_row(issued="2026-01-01", paid="2026-03-01")
    result = summarize_billing([row], TODAY)
    assert result["invoices"]["INV-1"]["fee"] == "0.00"
    assert result["invoices"]["INV-1"]["status"] == "paid"
