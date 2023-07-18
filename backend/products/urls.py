from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_create_view),
    path('<str:title>/', views.product_detail_view)
]
