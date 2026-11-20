import pytest
from rest_framework.test import APIClient

from tests.django.factories import UserFactory


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def api(user) -> APIClient:
    """An API client authenticated as `user`, without logging in."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client
