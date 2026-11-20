def send_once(
    store: KeyStore,
    key: str,
    message: EmailMessage,
    send: Callable[[EmailMessage], object],
) -> bool:
    """Send `message` unless it was already sent under `key`.

    Returns True if this call sent it, False if it had been sent before.

    Raises:
        TransientEmailError: If sending failed but may work later, or
            another worker is sending the same email right now.
        PermanentEmailError: If sending failed for good.
    """
    if not store.set(key, "sending", ex=CLAIM_SECONDS, nx=True):
        if store.get(key) == b"sent":
            return False
        raise TransientEmailError(f"{key} is being sent by another worker")
    try:
        send(message)
    except Exception as error:
        store.delete(key)  # let the next attempt claim it
        mapped = classify(error)
        if mapped is error:
            raise
        raise mapped from error
    store.set(key, "sent", ex=SENT_SECONDS)
    return True
