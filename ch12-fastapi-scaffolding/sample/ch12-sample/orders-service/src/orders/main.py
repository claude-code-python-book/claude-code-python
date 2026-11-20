"""The ASGI entrypoint for `fastapi dev`, `fastapi run` and Uvicorn."""

import logging

from orders.app import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
app = create_app()
