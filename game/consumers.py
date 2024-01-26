from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.urls import reverse
import json


class GameLobby(AsyncWebsocketConsumer):
    """
    Consumer for game
    """

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            match response['type']:
                case 'join':
                    current_username = self.scope['user'].username
                    room_code = response['room_code']
                    room_data = cache.get(room_code)
                    if not room_data:
                        print('Game not found')
                        return

                    if current_username == room_data['player1']:
                        await self.channel_layer.group_add(
                            room_code,
                            self.channel_name
                        )

                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'chat.message',
                                'message': 'first connected'
                            }
                        )
                    elif not room_data['player2']:
                        await self.channel_layer.group_add(
                            room_code,
                            self.channel_name
                        )
                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'chat.message',
                                'message': 'second connected'
                            }
                        )
                        # print(reverse('game', kwargs={'room_code': room_code}))
                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'chat.redirect',
                            }
                        )
                case 'move':
                    ...

    async def disconnect(self, code):
        print("WebSocket disconnected")

    async def chat_message(self, event):
        print("NICE", event)
        await self.send(text_data=json.dumps({
            'type': 'websocket.message',
            'message': event['message']
        }))

    async def chat_redirect(self, event):
        print("RED NICE", event)
        await self.send(text_data=json.dumps({
            'type': 'websocket.redirect',
        }))


