import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

pytestmark = pytest.mark.django_db
from user.tests.conftest import create_user, auth_client

class TestUserSignUp:

    def test_signup_success(self, api_client):
        # Arrange
        url = reverse("signup")
        payload = {
            "email": "newuser@example.com",
            "password": "StrongPass123!",
            "first_name": "New",
        }

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["message"] == "User registered successfully."

    def test_signup_duplicate_email(self, api_client, create_user):
        # Arrange
        create_user(email="dupe@example.com")
        url = reverse("signup")
        payload = {
            "email": "dupe@example.com",
            "password": "StrongPass123!",
            "first_name": "New",
        }

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_signup_missing_required_field(self, api_client):
        # Arrange
        url = reverse("signup")
        payload = {"email": "missing@example.com"}  # no password

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_signup_invalid_phone_number(self, api_client):
        # Arrange
        url = reverse("signup")
        payload = {
            "email": "phone@example.com",
            "password": "StrongPass123!",
            "first_name": "Test",
            "phone_number": "12345",  # invalid per validate_bd_phone_number
        }

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "phone_number" in response.data


class TestUserLogin:

    def test_login_success(self, api_client, create_user):
        # Arrange
        create_user(email="login@example.com", password="StrongPass123!")
        url = reverse("login")
        payload = {"email": "login@example.com", "password": "StrongPass123!"}

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.data
        assert "refresh_token" in response.data
        assert response.data["user"]["email"] == "login@example.com"

    def test_login_invalid_credentials(self, api_client, create_user):
        # Arrange
        create_user(email="login2@example.com", password="StrongPass123!")
        url = reverse("login")
        payload = {"email": "login2@example.com", "password": "WrongPass"}

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    def test_login_inactive_user(self, api_client, create_user):
        # Arrange
        user = create_user(email="inactive@example.com", password="StrongPass123!")
        user.is_active = False
        user.save()
        url = reverse("login")
        payload = {"email": "inactive@example.com", "password": "StrongPass123!"}

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        # Note: Django's ModelBackend excludes inactive users at authenticate()
        # time, so this currently hits "Invalid email or password" rather than
        # the "This account is inactive." branch in the serializer.
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_missing_fields(self, api_client):
        # Arrange
        url = reverse("login")
        payload = {"email": "x@example.com"}  # no password

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUserLogout:
        
    def test_logout_success(self, api_client, create_user):
        # Arrange
        user = create_user(
            email="logout@example.com",
            password="StrongPass123!"
        )

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )

        url = reverse("logout")
        payload = {"refresh_token": str(refresh)}

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_logout_invalid_token(self, api_client):
        # Arrange
        url = reverse("logout")
        payload = {"refresh_token": "not-a-real-token"}

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_already_blacklisted_token(self, api_client, create_user):
        # Arrange
        user = create_user(email="logout2@example.com", password="StrongPass123!")
        refresh = RefreshToken.for_user(user)
        refresh.blacklist()  # already blacklisted before the test even runs
        url = reverse("logout")
        payload = {"refresh_token": str(refresh)}

        # Act
        response = api_client.post(url, payload, format="json")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED