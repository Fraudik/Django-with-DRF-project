from django.urls import path, include
from .api.views import UserRegisterView, UserLoginView, UserUpdateView, UserConfirmOTPView
from .routers import users_router

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login first factor"),
    path('confirm-otp/', UserConfirmOTPView.as_view(), name="login second factor"),
    path('<int:id>/', UserUpdateView.as_view(), name="update"),
    path('', include(users_router.urls)),
] 
