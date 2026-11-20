"""Local development: debug on, mail printed to the console."""

from config.settings.base import *  # noqa: F403

DEBUG = True
SECRET_KEY = "dev-only-insecure-key"  # noqa: S105 - never used outside dev
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
