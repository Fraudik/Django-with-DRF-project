from rest_framework import serializers
from .models import ChatEvent
from users.serializers import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    owner = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ChatEvent
        fields = '__all__'
