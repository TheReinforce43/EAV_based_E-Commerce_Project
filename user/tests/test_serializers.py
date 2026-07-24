import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from user.Serializer.user_serializer import (
    UserSignUpSerializer,
    UserLoginSerializer,
    LogoutSerializer,
)
from utils.user_related import validate_bd_phone_number
from rest_framework import serializers 

User = get_user_model()


# ============================================================================
# 1. Helper Function Tests: validate_bd_phone_number
# ============================================================================

@pytest.mark.parametrize("input_number, expected_output", [
    ("01636021298", "01636021298"),
    ("+8801636021298", "01636021298"),
    ("8801636021298", "01636021298"),
    ("016 3602-1298", "01636021298"),
    ("+880 1711-000000", "01711000000"),
])
def test_validate_bd_phone_number_valid(input_number, expected_output):
    # Arrange — Done via parametrization

    # Act
    result = validate_bd_phone_number(input_number)

    # Assert
    assert result == expected_output


@pytest.mark.parametrize("invalid_number", [
    "01234567890",      # Operator digit '2' invalid in BD
    "0163602129",       # Too short (10 digits)
    "016360212989",     # Too long (12 digits)
    "+101636021298",    # Wrong country code
    "abc1636021298",    # Non-numeric characters
])
def test_validate_bd_phone_number_invalid(invalid_number):
    # Arrange — Done via parametrization

    # Act & Assert
    with pytest.raises(ValidationError):
        validate_bd_phone_number(invalid_number)


# ============================================================================
# 2. UserSignUpSerializer Tests
# ============================================================================

@pytest.mark.django_db
class TestUserSignUpSerializer:

    def test_signup_successful(self):
        # Arrange
        payload = {
            "email": "testuser@example.com",
            "password": "SecurePassword123!",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+8801711000000",
            "user_type": "customer",
            "address": "Dhaka, Bangladesh",
        }
        serializer = UserSignUpSerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()
        user = serializer.save()

        # Assert
        assert is_valid is True
        assert user.email == "testuser@example.com"
        assert user.first_name == "John"
        assert user.phone_number == "01711000000"  # Normalized format
        assert user.check_password("SecurePassword123!")  # Password hashed
        assert "password" not in serializer.data  # Write-only field excluded

    def test_duplicate_phone_number_fails(self):
        # Arrange
        User.objects.create_user(
            email="existing@example.com",
            password="Password123!",
            phone_number="01711000000"
        )
        payload = {
            "email": "newuser@example.com",
            "password": "Password123!",
            "phone_number": "+8801711000000",  # Same number, different format
        }
        serializer = UserSignUpSerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert is_valid is False
        assert "phone_number" in serializer.errors


# ============================================================================
# 3. UserLoginSerializer Tests
# ============================================================================

@pytest.mark.django_db
class TestUserLoginSerializer:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="login@example.com",
            password="CorrectPassword123!",
            first_name="Jane",
            user_type="customer"
        )

    def test_login_successful(self, user):
        # Arrange
        payload = {
            "email": "login@example.com",
            "password": "CorrectPassword123!"
        }
        serializer = UserLoginSerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()
        validated_data = serializer.validated_data

        # Assert
        assert is_valid is True
        assert "access_token" in validated_data
        assert "refresh_token" in validated_data
        assert validated_data["user"]["email"] == user.email

    def test_login_invalid_credentials(self, user):
        # Arrange
        payload = {
            "email": "login@example.com",
            "password": "WrongPassword!"
        }
        serializer = UserLoginSerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert is_valid is False
        assert "detail" in serializer.errors

    def test_login_inactive_user(self, user):
        # Arrange
        user.is_active = False
        user.save()

        payload = {
            "email": "login@example.com",
            "password": "CorrectPassword123!"
        }
        serializer = UserLoginSerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert is_valid is False
        assert "detail" in serializer.errors


# ============================================================================
# 4. LogoutSerializer Tests
# ============================================================================

@pytest.mark.django_db
class TestLogoutSerializer:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="logout@example.com",
            password="Password123!"
        )

    def test_logout_blacklists_token(self, user):
        # Arrange
        refresh = RefreshToken.for_user(user)
        refresh_str = str(refresh)
        payload = {"refresh_token": refresh_str}
        serializer = LogoutSerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()
        serializer.save()

        # Assert
        assert is_valid is True
        with pytest.raises(Exception):
            RefreshToken(refresh_str).check_blacklist()

    def test_logout_invalid_token(self):
        # Arrange
        payload = {"refresh_token": "invalid.jwt.token"}
        serializer = LogoutSerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert is_valid is True
        with pytest.raises(serializers.ValidationError):
            serializer.save()