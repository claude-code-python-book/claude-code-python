def test_convert_multiplies_and_rounds_half_up(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fx, "fetch_rates", lambda base, url: {"EUR": Decimal("1.15")})
    assert fx.convert(Decimal("10.30"), "GBP", "EUR") == Decimal("11.85")


def test_convert_to_the_same_currency_skips_the_service() -> None:
    with patch.object(fx, "fetch_rates") as fetch_rates:
        assert fx.convert(Decimal("5.00"), "GBP", "GBP") == Decimal("5.00")
    fetch_rates.assert_not_called()


def test_convert_rejects_an_unknown_currency(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(fx, "fetch_rates", lambda base, url: {"EUR": Decimal("1.15")})
    with pytest.raises(ValueError, match="no rate from GBP to JPY"):
        fx.convert(Decimal("1.00"), "GBP", "JPY")
