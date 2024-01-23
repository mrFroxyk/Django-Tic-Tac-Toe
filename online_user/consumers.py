import json
from channels.generic.websocket import AsyncWebsocketConsumer


class OnlineUser(AsyncWebsocketConsumer):
    """
    по факту для чата
    """

    async def connect(self):
        # await self.channel_layer.group_send(
        #     'all_chat',
        #     {
        #         'type':'chat.new_user'
        #     }
        # )

        await self.channel_layer.group_add(
            'all_chat',
            self.channel_name
        )
        await self.accept()
        print(self.scope)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            match response['type']:
                case 'message':
                    await self.channel_layer.group_send(
                        'all_chat',
                        {
                            'type': 'chat.message',
                            'message': response['message']
                        }
                    )

    async def disconnect(self, code):
        print("WebSocket disconnected")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'websocket.message',
            'message': event['message']
        }))

    async def chat_new_user(self, event):
        ...
