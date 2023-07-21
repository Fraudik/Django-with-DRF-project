from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegisterView

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('api/register', UserRegisterView.as_view()),
]
