def test_rejects_an_invoice_whose_rows_disagree_on_region(make_row: RowFactory) -> None:
    rows = [make_row(), make_row(region="DE")]
    result = summarize_billing(rows, TODAY)
    assert result["errors"] == ["row 3: invoice INV-1 changes"]
