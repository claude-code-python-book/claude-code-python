def test_accepts_payment_on_the_day_of_issue() -> None:
    row = BillingRow.model_validate({**VALID, "paid": VALID["issued"]})
    assert row.paid == row.issued
