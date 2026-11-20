"""One confirmation email, start to finish, with no Celery in sight.

The Celery task in notify/tasks.py only calls deliver_confirmation(), so
everything that can go wrong is tested here, without a broker.
"""

import asyncio
from collections.abc import Callable
from email.message import EmailMessage

from notify.delivery import KeyStore, PermanentEmailError, send_once
from notify.emails import confirmation_email
from notify.summary import OrderNotFoundError, Services, order_summary


def idempotency_key(order_id: int) -> str:
    """Return the key that marks this order's confirmation as sent."""
    return f"email:order-confirmation:{order_id}"


def deliver_confirmation(
    order_id: int,
    services: Services,
    store: KeyStore,
    send: Callable[[EmailMessage], object],
) -> bool:
    """Gather the data, build the email and send it once.

    Returns True if this call sent the email, False if it was already sent.

    Raises:
        PermanentEmailError: If the order doesn't exist or the address is bad.
        TransientEmailError: If sending should be retried later.
    """
    try:
        summary = asyncio.run(order_summary(services, order_id))
    except* OrderNotFoundError as group:
        raise PermanentEmailError(f"order {order_id} not found") from group
    message = confirmation_email(summary)
    return send_once(store, idempotency_key(order_id), message, send)
