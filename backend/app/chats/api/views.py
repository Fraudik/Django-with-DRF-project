from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import ChatEvent


class IndexView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'chats/index.html')


class ChatView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_name):
        full_chat_name = f'chat_{chat_name}'
        chats = list(ChatEvent.objects.filter(name=full_chat_name))
        if not chats:
            chat = ChatEvent(name=full_chat_name, user=request.user)
            chat.save()

        return render(request, 'chats/chat.html', {'chat_name': chat_name, 'chats': chats})
