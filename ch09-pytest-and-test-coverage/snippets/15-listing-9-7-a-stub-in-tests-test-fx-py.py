def test_fetch_rates_keeps_every_digit(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(url: str, timeout: float) -> io.BytesIO:
        return io.BytesIO(b'{"rates": {"EUR": 1.123456789012345678}}')

    monkeypatch.setattr(fx, "urlopen", fake_urlopen)
    assert fx.fetch_rates("GBP") == {"EUR": Decimal("1.123456789012345678")}
