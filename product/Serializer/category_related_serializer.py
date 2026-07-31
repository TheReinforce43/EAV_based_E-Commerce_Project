from rest_framework import serializers 
from product.Model.category_related_model import CategoryModel 


class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = CategoryModel 
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at']