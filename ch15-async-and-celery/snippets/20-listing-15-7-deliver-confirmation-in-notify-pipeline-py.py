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
