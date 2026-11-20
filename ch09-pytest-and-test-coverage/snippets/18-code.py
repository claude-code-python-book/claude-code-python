from unittest.mock import Mock, create_autospec

from invoicer.fx import fetch_rates

loose = Mock()
loose("GBP", "https://rates.test/latest", "EUR")  # accepted silently
print("Mock accepted three arguments")

strict = create_autospec(fetch_rates)
strict("GBP", "https://rates.test/latest", "EUR")  # fetch_rates takes two
