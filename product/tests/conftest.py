"""
Shared pytest fixtures for CategoryModel / CategorySerializer / CategoryViewSet tests.

ASSUMPTIONS (adjust to match your project):
- App is named `category`, so imports are `category.models` / `category.serializers`.
- Custom User model uses `email` as USERNAME_FIELD (per your existing setup),
  so `create_user` / `create_superuser` are called with `email=` + `password=`.
- CategoryViewSet is registered on a DRF router as:
    router.register(r'categories', CategoryViewSet, basename='category')
  which gives url names `category-list` and `category-detail`.
  If your basename differs, update `list_url()` / `detail_url()` in test_views.py.
"""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from product.Model.category_related_model import CategoryModel
import io 
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@example.com",
        password="AdminPass123!",
    )


@pytest.fixture
def normal_user(db):
    return User.objects.create_user(
        email="user@example.com",
        password="UserPass123!",
    )


@pytest.fixture
def category(db):
    return CategoryModel.objects.create(
        name="Electronics",
        description="Electronic items",
    )




def generate_test_image(fmt="JPEG"):
    """Return a real, valid in-memory image file (ImageField validates via Pillow,
    so raw fake bytes like b"fake-image-bytes" will fail validation silently)."""
    buffer = io.BytesIO()
    Image.new("RGB", (10, 10), color="red").save(buffer, format=fmt)
    buffer.seek(0)
    return SimpleUploadedFile(
        f"test_image.{fmt.lower()}", buffer.read(), content_type=f"image/{fmt.lower()}"
    )
 