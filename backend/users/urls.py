from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegisterView

urlpatterns = [
    path('login/', obtain_auth_token),
    path('register/', UserRegisterView.as_view()),
]
