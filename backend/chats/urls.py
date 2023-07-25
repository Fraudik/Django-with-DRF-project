from django.urls import path
from .api.views import IndexView, ChatView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:chat_name>/', ChatView.as_view(), name='chat'),
]
