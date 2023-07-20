from django.urls import path

from . import views, viewsets

urlpatterns = [
    path('', views.product_mixin_view, name='product-list'),
    path('<str:title>/', views.ProductMixinView.as_view(http_method_names=['post']), name='product-detail'),
    path('<str:title>/update/', viewsets.ProductViewSet.as_view({'put': "update"}), name='product-edit'),
    path('<str:title>/delete/', viewsets.ProductViewSet.as_view({'delete': "destroy"}), name='product-delete'),
]
