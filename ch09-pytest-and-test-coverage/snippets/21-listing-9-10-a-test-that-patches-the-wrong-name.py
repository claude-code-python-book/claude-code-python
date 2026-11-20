from unittest.mock import patch

from invoicer import fx


def test_fetch_rates_patched_in_the_wrong_place() -> None:
    with patch("urllib.request.urlopen") as urlopen:
        urlopen.return_value.__enter__.return_value.read.return_value = b'{"rates": {}}'
        assert fx.fetch_rates("GBP", "https://rates.invalid/latest") == {}
