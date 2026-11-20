# pytest patterns

Six complete examples. Copy the one you need and adapt the names.

## 1. A fixture for shared setup

```python
import pytest

from shop.pricing import Cart


@pytest.fixture
def cart() -> Cart:
    cart = Cart()
    cart.add("book", 20.0, quantity=2)
    return cart


def test_total_counts_quantities(cart: Cart) -> None:
    assert cart.total() == 40.0
```

## 2. Expected exceptions

```python
import pytest

from shop.pricing import parse_quantity


def test_parse_quantity_rejects_zero() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        parse_quantity("0")
```

## 3. Floating-point results

```python
import pytest


def test_tenth_plus_two_tenths() -> None:
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

## 4. Temporary files

```python
from pathlib import Path


def test_writes_a_report(tmp_path: Path) -> None:
    report = tmp_path / "report.txt"
    report.write_text("total=40.0", encoding="utf-8")
    assert report.read_text(encoding="utf-8") == "total=40.0"
```

## 5. Environment variables

```python
import os

import pytest


def test_reads_the_currency(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SHOP_CURRENCY", "EUR")
    assert os.environ["SHOP_CURRENCY"] == "EUR"
```

## 6. Replacing a slow or external call

```python
from unittest.mock import Mock


def fetch_rate(client: Mock) -> float:
    return client.get_rate("EUR")


def test_fetch_rate_uses_the_client() -> None:
    client = Mock()
    client.get_rate.return_value = 1.08
    assert fetch_rate(client) == 1.08
    client.get_rate.assert_called_once_with("EUR")
```
