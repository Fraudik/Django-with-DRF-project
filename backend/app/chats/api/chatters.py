import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ..models import ChatEvent


class ChatUser(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_name = None

    async def connect(self):
        self.chat_name = f"chat_{self.scope['url_route']['kwargs']['chat_name']}"
        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        await self.accept()

    async def disconnect(self, **kwargs):
        await self.channel_layer.group_discard(self.chat_name, self.channel_name)

    async def receive(self, text_data=None, byte_data=None):
        if text_data is None:
            return

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = self.scope['user'].id

        chat_name = await database_sync_to_async(ChatEvent.objects.get)(name=self.chat_name)

        chat = ChatEvent(
            content=message,
            user=self.scope['user'],
            name=chat_name,
        )

        await database_sync_to_async(chat.save)()

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': user_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        await self.send(text_data=json.dumps(
                {
                    'message': message,
                    'user_id': user_id,
                }
            ))
