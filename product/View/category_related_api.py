from utils.custom_permission import isAdminOrReadOnly 

from rest_framework.viewsets import ModelViewSet 
from product.Model.category_related_model import CategoryModel
from product.Serializer.category_related_serializer import CategorySerializer 



class CategoryViewSet(ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [isAdminOrReadOnly]