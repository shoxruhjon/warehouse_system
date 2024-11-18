from rest_framework.urls import path
from .views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView
)

urlpatterns = [
    path('products/create/', ProductCreateView.as_view()),
    path('products/delete/<uuid:id>', ProductDeleteView.as_view()),
    path('products/detail/<uuid:id>', ProductDetailView.as_view()),
    path('products/', ProductListView.as_view()),
]