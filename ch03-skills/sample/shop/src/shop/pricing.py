"""Prices, discounts and a simple shopping cart."""
from dataclasses import dataclass, field

def apply_discount(price: float, percent: float) -> float:
    """Return the price after a percentage discount, rounded to 2 places."""
    if price < 0:
        raise ValueError("price cannot be negative")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)

def parse_quantity(text: str) -> int:
    """Parse a quantity typed by a user, such as ' 3 '."""
    value = int(text.strip())  # int() raises ValueError for non-numbers
    if value < 1:
        raise ValueError("quantity must be at least 1")
    return value

@dataclass
class Cart:
    """A shopping cart that maps item names to (price, quantity)."""

    items: dict[str, tuple[float, int]] = field(default_factory=dict)

    def add(self, name: str, price: float, quantity: int = 1) -> None:
        """Add an item, or increase its quantity if it is already in the cart."""
        if quantity < 1:
            raise ValueError("quantity must be at least 1")
        _, old_quantity = self.items.get(name, (price, 0))
        self.items[name] = (price, old_quantity + quantity)

    def total(self, discount_percent: float = 0) -> float:
        """Return the cart total after an optional percentage discount."""
        subtotal = sum(price * qty for price, qty in self.items.values())
        return apply_discount(subtotal, discount_percent)
