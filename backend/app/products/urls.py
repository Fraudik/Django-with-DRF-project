from django.urls import path

from .api import views, viewsets

urlpatterns = [
    path('', views.ProductMixinView.as_view(), name='product-list'),
    path('<str:title>/', views.ProductMixinView.as_view(http_method_names=['get']), name='product-detail'),
    path('<str:title>/update/', viewsets.ProductViewSet.as_view({'put': "update"}), name='product-edit'),
    path('<str:title>/delete/', viewsets.ProductViewSet.as_view({'delete': "destroy"}), name='product-delete'),
]
