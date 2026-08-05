"""
API tests for CategoryViewSet, exercising the isAdminOrReadOnly permission:
- Safe methods (GET/HEAD/OPTIONS): allowed for anyone, including anonymous users.
- Unsafe methods (POST/PUT/PATCH/DELETE): allowed only for superusers.

If your router uses a different `basename`, update list_url()/detail_url() below.
"""

import pytest
from django.urls import reverse
from rest_framework import status

from product.Model.category_related_model import CategoryModel


def list_url():
    return reverse("category-list")


def detail_url(pk):
    return reverse("category-detail", kwargs={"pk": pk})


@pytest.mark.django_db
class TestCategoryListCreateAPI:

    def test_anonymous_user_can_list_categories(self, api_client, category):
        # Arrange
        url = list_url()

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_non_admin_can_list_categories(self, api_client, normal_user, category):
        # Arrange
        api_client.force_authenticate(user=normal_user)
        url = list_url()

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_anonymous_user_cannot_create_category(self, api_client):
        # Arrange
        payload = {"name": "New Category"}

        # Act
        response = api_client.post(list_url(), payload)

        # Assert
        # DRF returns 401 for unauthenticated requests when the auth backend
        # (e.g. JWT) issues a challenge, or 403 depending on config — either
        # is a valid "not allowed" response here.
        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )
        assert not CategoryModel.objects.filter(name="New Category").exists()

    def test_non_admin_user_cannot_create_category(self, api_client, normal_user):
        # Arrange
        api_client.force_authenticate(user=normal_user)
        payload = {"name": "New Category"}

        # Act
        response = api_client.post(list_url(), payload)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CategoryModel.objects.filter(name="New Category").exists()

    def test_admin_user_can_create_category(self, api_client, admin_user):
        # Arrange
        api_client.force_authenticate(user=admin_user)
        payload = {"name": "New Category", "description": "desc"}

        # Act
        response = api_client.post(list_url(), payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert CategoryModel.objects.filter(name="New Category").exists()

    def test_admin_create_with_missing_name_returns_400(self, api_client, admin_user):
        # Arrange
        api_client.force_authenticate(user=admin_user)
        payload = {}

        # Act
        response = api_client.post(list_url(), payload)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCategoryDetailAPI:

    def test_anonymous_user_can_retrieve_category(self, api_client, category):
        # Arrange
        url = detail_url(category.pk)

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == category.name

    def test_retrieve_nonexistent_category_returns_404(self, api_client):
        # Arrange
        url = detail_url(999999)

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_non_admin_user_cannot_update_category(self, api_client, normal_user, category):
        # Arrange
        api_client.force_authenticate(user=normal_user)
        payload = {"name": "Updated"}

        # Act
        response = api_client.patch(detail_url(category.pk), payload)
        category.refresh_from_db()

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert category.name != "Updated"

    def test_admin_user_can_update_category(self, api_client, admin_user, category):
        # Arrange
        api_client.force_authenticate(user=admin_user)
        payload = {"name": "Updated"}

        # Act
        response = api_client.patch(detail_url(category.pk), payload)
        category.refresh_from_db()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert category.name == "Updated"

    def test_anonymous_user_cannot_delete_category(self, api_client, category):
        # Arrange
        url = detail_url(category.pk)

        # Act
        response = api_client.delete(url)

        # Assert
        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )
        assert CategoryModel.objects.filter(pk=category.pk).exists()

    def test_non_admin_user_cannot_delete_category(self, api_client, normal_user, category):
        # Arrange
        api_client.force_authenticate(user=normal_user)
        url = detail_url(category.pk)

        # Act
        response = api_client.delete(url)

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CategoryModel.objects.filter(pk=category.pk).exists()

    def test_admin_user_can_delete_category(self, api_client, admin_user, category):
        # Arrange
        api_client.force_authenticate(user=admin_user)
        url = detail_url(category.pk)

        # Act
        response = api_client.delete(url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CategoryModel.objects.filter(pk=category.pk).exists()