@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("unit_price", "NaN", "finite number"),
        ("unit_price", "Infinity", "finite number"),
        ("unit_price", "-0.01", "greater than or equal to 0"),
        ("customer", "   ", "at least 1 character"),
        ("region", "uk", "Input should be 'UK'"),
        ("qty", "1e2", "whole number"),
        ("issued", "2026-02-29", "YYYY-MM-DD"),
    ],
)
def test_rejects_invalid_values(field: str, value: str, message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        BillingRow.model_validate({**VALID, field: value})


@pytest.mark.parametrize(
    ("field", "value"), [("unit_price", "0"), ("issued", "2028-02-29")]
)
def test_accepts_boundary_values(field: str, value: str) -> None:
    row = BillingRow.model_validate({**VALID, field: value})
    assert str(getattr(row, field)) == value
