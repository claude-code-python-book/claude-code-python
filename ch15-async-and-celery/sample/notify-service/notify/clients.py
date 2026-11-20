"""The real services, over HTTP with httpx."""

import os
from decimal import Decimal
from typing import Self

import httpx

from notify.summary import Order, OrderNotFoundError


class HttpServices:
    """Calls the orders, shipping and loyalty services' JSON APIs."""

    def __init__(self, orders: str, shipping: str, loyalty: str) -> None:
        self.urls = {"orders": orders, "shipping": shipping, "loyalty": loyalty}

    @classmethod
    def from_env(cls) -> Self:
        """Read the three base URLs from the environment."""
        return cls(
            os.environ["ORDERS_URL"],
            os.environ["SHIPPING_URL"],
            os.environ["LOYALTY_URL"],
        )

    async def _get(self, service: str, path: str, **params: str) -> httpx.Response:
        async with httpx.AsyncClient(base_url=self.urls[service], timeout=5) as client:
            return await client.get(path, params=params)

    async def order(self, order_id: int) -> Order:
        """Load one order; raise OrderNotFoundError on 404."""
        response = await self._get("orders", f"/orders/{order_id}")
        if response.status_code == httpx.codes.NOT_FOUND:
            raise OrderNotFoundError(order_id)
        response.raise_for_status()
        data = response.json()
        lines = tuple(
            (line["item"], line["quantity"], Decimal(line["price"]))
            for line in data["lines"]
        )
        return Order(
            data["id"], data["email"], data["name"], Decimal(data["total"]), lines
        )

    async def delivery_estimate(self, order_id: int) -> str:
        """Return a human-readable delivery date."""
        response = await self._get("shipping", f"/estimates/{order_id}")
        response.raise_for_status()
        return str(response.json()["label"])

    async def loyalty_points(self, email: str) -> int:
        """Return the customer's points balance."""
        response = await self._get("loyalty", "/balances", email=email)
        response.raise_for_status()
        return int(response.json()["points"])
