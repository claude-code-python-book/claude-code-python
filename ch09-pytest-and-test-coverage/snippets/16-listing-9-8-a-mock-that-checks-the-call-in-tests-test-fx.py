def test_fetch_rates_asks_for_the_base_currency() -> None:
    with patch("invoicer.fx.urlopen") as urlopen:
        response = urlopen.return_value.__enter__.return_value
        response.read.return_value = b'{"rates": {}}'
        fx.fetch_rates("GBP", "https://rates.test/latest")
    urlopen.assert_called_once_with("https://rates.test/latest?base=GBP", timeout=5)
