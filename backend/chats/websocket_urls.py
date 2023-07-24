from django.urls import re_path
from .api.chatters import ChatUser

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatUser.as_asgi())
]
