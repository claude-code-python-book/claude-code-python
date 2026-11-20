"""Production: every secret comes from the environment; startup fails without it."""

import os

from config.settings.base import *  # noqa: F403

DEBUG = False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = os.environ["DJANGO_ALLOWED_HOSTS"].split(",")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "bookings@example.com")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600  # raise to a year once HTTPS is confirmed everywhere
