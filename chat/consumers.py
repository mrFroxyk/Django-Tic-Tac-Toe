import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Consumer for chat
    """

    async def connect(self):
        await self.channel_layer.group_add(
            'all_chat',
            self.channel_name,
        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            match response['type']:
                case 'message':
                    username = self.scope['user'].username
                    await self.channel_layer.group_send(
                        'all_chat',
                        {
                            'type': 'chat.message',
                            'message': f"{username}: {response['message']}"
                        }
                    )

    async def disconnect(self, code):
        print("WebSocket disconnected")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'websocket.message',
            'message': event['message']
        }))
