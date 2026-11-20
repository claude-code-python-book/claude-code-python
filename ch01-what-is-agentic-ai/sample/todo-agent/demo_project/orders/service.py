"""Order service for the demo."""


def place_order(order_id: str) -> str:
    # TODO: add retry when the payment gateway times out
    return f"placed {order_id}"
