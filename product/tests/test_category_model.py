import pytest 
from product.Model.category_related_model import CategoryModel 


@pytest.mark.django_db
class TestCategoryModel:

    def test_create_category_with_required_field_only(self):
        # Arrange
        name = "Books"

        # Act
        category = CategoryModel.objects.create(name=name)

        # Assert
        assert category.pk is not None
        assert category.name == name

    def test_description_and_image_are_optional(self):
        # Arrange
        name = "Toys"

        # Act
        category = CategoryModel.objects.create(name=name)

        # Assert
        assert category.description in (None, "")
        assert not category.image

    def test_str_returns_name(self):
        # Arrange
        category = CategoryModel.objects.create(name="Furniture")

        # Act
        result = str(category)

        # Assert
        assert result == "Furniture"

    def test_created_at_and_updated_at_are_auto_set(self):
        # Arrange
        name = "Sports"

        # Act
        category = CategoryModel.objects.create(name=name)

        # Assert
        assert category.created_at is not None
        assert category.updated_at is not None

    def test_updated_at_changes_on_save(self):
        # Arrange
        category = CategoryModel.objects.create(name="Music")
        original_updated_at = category.updated_at

        # Act
        category.name = "Musical Instruments"
        category.save()
        category.refresh_from_db()

        # Assert
        assert category.updated_at > original_updated_at

    def test_created_at_does_not_change_on_save(self):
        # Arrange
        category = CategoryModel.objects.create(name="Garden")
        original_created_at = category.created_at

        # Act
        category.name = "Gardening"
        category.save()
        category.refresh_from_db()

        # Assert
        assert category.created_at == original_created_at

    def test_multiple_categories_can_share_name(self):
        # Arrange
        name = "Duplicate"

        # Act
        CategoryModel.objects.create(name=name)
        CategoryModel.objects.create(name=name)

        # Assert
        # No unique constraint on `name` in the model, so this should succeed.
        assert CategoryModel.objects.filter(name=name).count() == 2