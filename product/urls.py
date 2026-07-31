from django.urls import path ,include 

from rest_framework import routers
from product.View.category_related_api import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
]