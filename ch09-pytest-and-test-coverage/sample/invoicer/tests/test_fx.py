import io
from decimal import Decimal
from unittest.mock import patch

import pytest

from invoicer import fx


def test_fetch_rates_reads_the_rates_service(rates_server: str) -> None:
    rates = fx.fetch_rates("GBP", rates_server)
    assert rates == {"EUR": Decimal("1.15"), "USD": Decimal("1.27")}


def test_fetch_rates_keeps_every_digit(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(url: str, timeout: float) -> io.BytesIO:
        return io.BytesIO(b'{"rates": {"EUR": 1.123456789012345678}}')

    monkeypatch.setattr(fx, "urlopen", fake_urlopen)
    assert fx.fetch_rates("GBP") == {"EUR": Decimal("1.123456789012345678")}


def test_fetch_rates_asks_for_the_base_currency() -> None:
    with patch("invoicer.fx.urlopen") as urlopen:
        response = urlopen.return_value.__enter__.return_value
        response.read.return_value = b'{"rates": {}}'
        fx.fetch_rates("GBP", "https://rates.test/latest")
    urlopen.assert_called_once_with("https://rates.test/latest?base=GBP", timeout=5)


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
