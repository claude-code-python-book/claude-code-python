def post(message: str, token: str) -> None:
    request = Request(
        WEBHOOK_URL,
        data=message.encode(),
        headers={"Authorization": f"Bearer {token}"},
    )
    # WEBHOOK_URL is a fixed https URL, so urlopen can't be sent to file: URLs.
    with urlopen(request, timeout=5):  # noqa: S310
        pass


async def post_all(
    messages: Iterable[str], token: str, delay: float = 1.0
) -> list[str]:
    """Post each message, at most one per `delay` seconds; return the failures."""
    failed: list[str] = []
    for message in messages:
        try:
            await asyncio.to_thread(post, message, token)
        except URLError as error:
            log.warning("reminder not sent: %s", error)
            failed.append(message)
        await asyncio.sleep(delay)
    return failed
