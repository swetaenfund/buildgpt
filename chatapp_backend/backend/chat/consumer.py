from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from chat.models import Chat

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        chat_with_user = self.scope['url_route']['kwargs']['id']
        user_ids = [int(self.scope['user'].id), int(chat_with_user)]
        user_ids = sorted(user_ids)
        self.room_group_name = f"chat_{user_ids}-{user_ids}"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send any stored messages to the user
        await self.send_stored_messages()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id
            }
        )
        await self.save_message_to_db(sender_id, self.room_group_name, message)

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        await self.send(text_data=json.dumps({
            "message": message,
            "sender_id": sender_id
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message_to_db(self, sender_id, thread_name, message):
        chat_obj = Chat.objects.create(sender_id=sender_id, thread_name=thread_name, message=message)

    @database_sync_to_async
    def get_stored_messages(self):
        return Chat.objects.filter(thread_name=self.room_group_name).order_by('message_time')

    async def send_stored_messages(self):
        messages = await self.get_stored_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                "message": message.message,
                "sender_id": message.sender_id
            }))
