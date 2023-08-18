from rest_framework.routers import DefaultRouter
from .api.viewsets import UserFetchDeleteViewSet

users_router = DefaultRouter()
users_router.register(r'', UserFetchDeleteViewSet, basename="user")
