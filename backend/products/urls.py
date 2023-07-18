from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_mixin_view),
    path('<str:title>/', views.product_mixin_view),
    path('<str:title>/update/', views.product_mixin_view),
    path('<str:title>/delete/', views.product_mixin_view),
]
