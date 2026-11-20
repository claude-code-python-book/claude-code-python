"""Tests: like dev, with a fast password hasher."""

from config.settings.dev import *  # noqa: F403

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
