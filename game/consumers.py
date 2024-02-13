from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import asyncio
import json
import time


class GameLobby(AsyncWebsocketConsumer):
    """
    Consumer for the game lobby. The user is redirected here from
    game_create view and will be redirected to game (play) when
    he finds an opponent
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
                        room_data['player2'] = self.scope['user'].username
                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'chat.redirect',
                            }
                        )
                        room_data['time_last_action'] = int(time.time()) + 1
                        cache.set(room_code, room_data)

    async def disconnect(self, code):
        print("WebSocket disconnected")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'websocket.message',
            'message': event['message']
        }))

    async def chat_redirect(self, event):
        await self.send(text_data=json.dumps({
            'type': 'websocket.redirect',
        }))


class Game(AsyncWebsocketConsumer):
    """
    Consumer for game
    """

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            print(response)
            room_code = response['room_code']
            match response['type']:
                case 'join':
                    await self.channel_layer.group_add(
                        room_code,
                        self.channel_name
                    )
                    room_data = cache.get(room_code)

                    # Correct the time of move if a connection occurs between moves
                    time_delta = int(time.time()) - room_data['time_last_action']
                    match room_data['current_player']:
                        case 'player1':
                            room_data['player1_time'] -= time_delta
                        case 'player2':
                            room_data['player2_time'] -= time_delta
                    await self.send(
                        text_data=json.dumps(room_data)
                    )

                case 'move':
                    room_data = cache.get(room_code)
                    username = self.scope['user'].username

                    if username != room_data[room_data['current_player']]:
                        return

                    if username == room_data['player1']:
                        user_num = 'player1'
                        enemy_user_num = 'player2'
                    if username == room_data['player2']:
                        user_num = 'player2'
                        enemy_user_num = 'player1'

                    move_id = int(response['position'])
                    border_to_render = room_data['border_to_render']
                    current_move = room_data['current_move']
                    if border_to_render[move_id] == '':
                        border_to_render[move_id] = current_move
                        room_data['current_player'] = enemy_user_num
                        time_delta = int(time.time()) - room_data['time_last_action']
                        room_data['time_last_action'] = int(time.time())
                        match room_data['current_player']:
                            case 'player1':
                                room_data['player2_time'] -= time_delta
                            case 'player2':
                                room_data['player1_time'] -= time_delta

                        await self.channel_layer.group_send(
                            room_code, room_data
                        )
                        if current_move == 'X':
                            current_move = 'O'
                        else:
                            current_move = 'X'

                        room_data['current_move'] = current_move
                        room_data['border_to_render'] = border_to_render
                        cache.set(room_code, room_data)

    async def disconnect(self, code):
        ...

    async def game_move(self, event):
        event['type'] = 'websocket.render'
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def check_end(second):
        await asyncio.sleep(second)
        print("task completed")
