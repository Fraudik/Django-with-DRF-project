from django.urls import path
from .api.views import Index, Chat

urlpatterns = [
    path('', Index.as_view(), name='main'),
    path('<str:chat_name>/', Chat.as_view(), name='chat'),
]
