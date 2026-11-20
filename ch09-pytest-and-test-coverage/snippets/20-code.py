from decimal import Decimal

from pytest_mock import MockerFixture

from invoicer import fx


def test_convert_asks_for_rates_once(mocker: MockerFixture) -> None:
    rates = {"EUR": Decimal("1.15")}
    fetch = mocker.patch("invoicer.fx.fetch_rates", return_value=rates)
    assert fx.convert(Decimal("10.30"), "GBP", "EUR") == Decimal("11.85")
    fetch.assert_called_once_with("GBP", fx.RATES_URL)
