import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Count, F, Value
from channels.db import database_sync_to_async
# from main_app.models import Chat, Thread
from .models import Esp32, RFID

class WriteToRFID(AsyncWebsocketConsumer):
    """
    Write RFID data
    """
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['esp_name']

        self.room_group_name = "chat_%s" % self.room_name

        print("connected")
        print("channel layer", self.channel_layer)
        print("channel layer alias", self.channel_layer_alias)
        print("goup name", self.room_group_name)
        print("channel name", self.channel_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, event):
        print("disconnected")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "chat.message",
                'message': text_data
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=event['message']
        )
        

    # async def save_chat(self, send_user_pk, recieve_user_pk):
    #     Thread.objects.
    #     return Chat.objects.create(send_user=)


class SendRfidDataToESP(AsyncWebsocketConsumer):
    """
    send RFID data to esp32 when getting the request
    """
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['esp_name']

        self.room_group_name = "chat_%s" % self.room_name

        print("connected")
        print("channel layer", self.channel_layer)
        print("channel layer alias", self.channel_layer_alias)
        print("goup name", self.room_group_name)
        print("channel name", self.channel_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, event):
        print("disconnected")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': "chat.message",
                'message': text_data
            }
        )

    async def chat_message(self, event):
        await self.send(
            text_data=event['message']
        )


     