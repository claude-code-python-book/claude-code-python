"""Tests for shop.pricing, written with the writing-pytest-tests skill."""
import pytest

from shop.pricing import Cart, apply_discount, parse_quantity

@pytest.mark.parametrize(
    ("price", "percent", "expected"),
    [(100.0, 10, 90.0), (19.99, 0, 19.99), (50.0, 100, 0.0), (10.0, 33, 6.7)],
)
def test_apply_discount_returns_discounted_price(price, percent, expected):
    assert apply_discount(price, percent) == expected

def test_apply_discount_rejects_negative_price():
    with pytest.raises(ValueError, match="negative"):
        apply_discount(-1.0, 10)

@pytest.mark.parametrize("percent", [-5, 101])
def test_apply_discount_rejects_percent_out_of_range(percent):
    with pytest.raises(ValueError, match="between 0 and 100"):
        apply_discount(100.0, percent)

@pytest.mark.parametrize(("text", "expected"), [("3", 3), (" 12 ", 12)])
def test_parse_quantity_accepts_whole_numbers(text, expected):
    assert parse_quantity(text) == expected

@pytest.mark.parametrize("text", ["0", "-2", "abc", ""])
def test_parse_quantity_rejects_invalid_input(text):
    with pytest.raises(ValueError):
        parse_quantity(text)

@pytest.fixture
def cart():
    return Cart()

def test_cart_add_combines_quantities(cart):
    cart.add("pen", 1.5)
    cart.add("pen", 1.5, quantity=2)
    assert cart.items["pen"] == (1.5, 3)

def test_cart_add_rejects_zero_quantity(cart):
    with pytest.raises(ValueError, match="at least 1"):
        cart.add("pen", 1.5, quantity=0)

def test_cart_total_applies_discount(cart):
    cart.add("book", 20.0, quantity=2)
    cart.add("pen", 5.0)
    assert cart.total(discount_percent=10) == 40.5

def test_cart_total_of_empty_cart_is_zero(cart):
    assert cart.total() == 0.0
