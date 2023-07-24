from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self, request):
        return render(request, 'chats/index.html')


class Chat(View):
    def get(self, request, chat_name):
        return render(request, 'chats/chat.html', {'chat_name': chat_name})
