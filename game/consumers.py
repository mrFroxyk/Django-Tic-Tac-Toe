from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import json


# class GameManagerConsumer(AsyncWebsocketConsumer):
#
#     async def connect(self):
#         self.channel_layer.group_add(
#             "all_chat",
#             self.channel_name
#         )
#         await self.accept()

# async def receive(self, text_data=None, bytes_data=None):
#     if text_data:
#         response = json.loads(text_data)
#         print(response)
#         await self.send(text_data=json.dumps({
#             'type': 'websocket.message',
#             'message': 'message'
#         }))
#
#         match response['type']:
#             case 'message':
#                 print(2)
#                 await self.channel_layer.group_send(
#                     "all_chat",
#                     {
#                         'type': 'chat.message',
#                         'message': '123',
#                     }
#                 )
#                 print("end sending")
#
# async def disconnect(self, code):
#     print("disconnect")
#
# async def chat_message(self, event):
#     print("NICE")
#     message = event['message']
#
#     # Send message to WebSocket
#     await self.send(text_data=json.dumps({
#         'type': 'websocket.message',
#         'message': message
#     }))


class GameManagerConsumer(AsyncWebsocketConsumer):
    """
    Consumer for chat
    """

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            # print(response)
            match response['type']:
                case 'join':
                    current_username = self.scope['user'].username
                    room_code = response['room_code']
                    room_data = cache.get(room_code)
                    if current_username == room_data['player1']:
                        print(room_code, self.channel_name)
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
                        print('типа начал рассылку')
                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'chat.message',
                                'message': 'second connect'
                            }
                        )

    async def disconnect(self, code):
        print("WebSocket disconnected")

    async def chat_message(self, event):
        print("NICE", event)
        await self.send(text_data=json.dumps({
            'type': 'websocket.message',
            'message': event['message']
        }))
