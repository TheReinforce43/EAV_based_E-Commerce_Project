import pytest

from  product.tests.conftest import generate_test_image 
from product.Serializer.category_related_serializer import CategorySerializer

import io



@pytest.mark.django_db
class TestCategorySerializer:

    def test_contains_expected_fields(self, category):
        # Arrange
        serializer = CategorySerializer(instance=category)

        # Act
        data = serializer.data

        # Assert
        assert set(data.keys()) == {
            "id", "name", "description", "image", "created_at", "updated_at",
        }

    def test_serialized_data_matches_instance(self, category):
        # Arrange
        serializer = CategorySerializer(instance=category)

        # Act
        data = serializer.data

        # Assert
        assert data["name"] == category.name
        assert data["description"] == category.description

    def test_valid_payload_creates_category(self):
        # Arrange
        payload = {"name": "Kitchen", "description": "Kitchenware"}
        serializer = CategorySerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()
        instance = serializer.save()

        # Assert
        assert is_valid, serializer.errors
        assert instance.name == "Kitchen"

    def test_missing_name_is_invalid(self):
        # Arrange
        payload = {"description": "No name provided"}
        serializer = CategorySerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert not is_valid
        assert "name" in serializer.errors

    def test_blank_name_is_invalid(self):
        # Arrange
        payload = {"name": ""}
        serializer = CategorySerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert not is_valid
        assert "name" in serializer.errors

    def test_blank_description_is_allowed(self):
        # Arrange
        payload = {"name": "Outdoor", "description": ""}
        serializer = CategorySerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert is_valid, serializer.errors

    def test_missing_description_is_allowed(self):
        # Arrange
        payload = {"name": "Outdoor"}
        serializer = CategorySerializer(data=payload)

        # Act
        is_valid = serializer.is_valid()

        # Assert
        assert is_valid, serializer.errors


    def test_image_upload_is_accepted(self):
        # Arrange
        payload = {"name": "Photography", "image": generate_test_image()}
        serializer = CategorySerializer(data=payload)
 
        # Act
        is_valid = serializer.is_valid()
 
        # Assert
        assert is_valid, serializer.errors
        instance = serializer.save()
        assert bool(instance.image) is True

  

    def test_update_preserves_id(self, category):
        # Arrange
        payload = {"name": "Renamed Category", "id": 99999}
        serializer = CategorySerializer(instance=category, data=payload)

        # Act
        is_valid = serializer.is_valid()
        updated = serializer.save()

        # Assert
        assert is_valid, serializer.errors
        assert updated.id == category.id
        assert updated.name == "Renamed Category"

    def test_name_exceeding_max_length_is_invalid(self):
        # Arrange
        payload = {"name": "x" * 256}  # max_length is 255

        # Act
        serializer = CategorySerializer(data=payload)
        is_valid = serializer.is_valid()

        # Assert
        assert not is_valid
        assert "name" in serializer.errors