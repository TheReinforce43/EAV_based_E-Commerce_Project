import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User  # adjust import path


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def _create_user(**kwargs):
        defaults = {
            "email": "testuser@example.com",
            "password": "StrongPass123!",
            "first_name": "Test",
        }
        defaults.update(kwargs)
        password = defaults.pop("password")
        user = User.objects.create_user(password=password, **defaults)
        return user
    return _create_user


@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client, user, refresh