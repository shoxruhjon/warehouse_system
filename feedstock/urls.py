from rest_framework.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    MaterialCreateView,
    MaterialDeleteView,
    MaterialDetailView,
    MaterialListView,
    ProductMaterialViewSet,
    WarehouseViewSet, ProductMaterialSupplyView
)

router = DefaultRouter()
router.register(r'product-materials', ProductMaterialViewSet)
router.register(r'warehouses', WarehouseViewSet)
urlpatterns = [
    path('products/create/', ProductCreateView.as_view()),
    path('products/delete/<uuid:id>', ProductDeleteView.as_view()),
    path('products/detail/<uuid:id>', ProductDetailView.as_view()),
    path('products/', ProductListView.as_view()),
    path('materials/create/', MaterialCreateView.as_view()),
    path('materials/delete/<uuid:id>', MaterialDeleteView.as_view()),
    path('materials/detail/<uuid:id>', MaterialDetailView.as_view()),
    path('materials/', MaterialListView.as_view()),
    path('', include(router.urls)),
    path('products/materials/supply/', ProductMaterialSupplyView.as_view()),
]
