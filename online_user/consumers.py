from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer


class OnlineUser(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['user'], "<<<<<user")
        await self.accept()
        print("WebSocket connected", self.channel_layer)

    async def receive(self, text_data=None, bytes_data=None):
        channel = get_channel_layer()
        print(channel)
        if text_data:
            print("Received message:", text_data)
            await self.send(text_data="Message received")

    async def disconnect(self, code):
        print("WebSocket disconnected")
