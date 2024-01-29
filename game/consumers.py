from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.urls import reverse
from urllib.parse import parse_qs
import json


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
                        cache.set(room_code, room_data)
                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'chat.redirect',
                            }
                        )

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

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.enemy_user_num = None
        self.username = None
        self.user_num = None
        self.room_code = None

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            print(response)
            print(self.scope['user'], self.scope['user'].username)
            match response['type']:
                case 'join':
                    self.room_code = response['room_code']
                    await self.channel_layer.group_add(
                        self.room_code,
                        self.channel_name
                    )
                    username = self.scope['user'].username
                    # Хули блять ты не работаешь
                    room_data = cache.get(self.room_code)
                    # print(username, room_data['player1'], room_data['player2'])
                    if username == room_data['player1']:
                        self.user_num = 'player1'
                        self.enemy_user_num = 'player2'
                    elif username == room_data['player2']:
                        self.user_num = 'player2'
                        self.enemy_user_num = 'player1'

                    border_to_render = room_data['border_to_render']
                    await self.channel_layer.group_send(
                        self.room_code,
                        {
                            'type': 'game.move',
                            'border_to_render': border_to_render
                        }
                    )

                case 'move':
                    game_data = cache.get(self.room_code)
                    print(self.user_num, game_data['current_player'])
                    if self.user_num != game_data['current_player']:
                        return
                    move_id = int(response['position'])

                    border_to_render = game_data['border_to_render']
                    current_move = game_data['current_move']
                    if border_to_render[move_id] == '':
                        border_to_render[move_id] = current_move
                        await self.channel_layer.group_send(
                            self.room_code,
                            {
                                'type': 'game.move',
                                'border_to_render': border_to_render
                            }
                        )
                        if current_move == 'X':
                            current_move = 'O'
                        else:
                            current_move = 'X'
                        game_data['current_move'] = current_move
                        game_data['border_to_render'] = border_to_render
                        print(game_data)
                        cache.set(self.room_code, game_data)

    async def disconnect(self, code):
        ...

    async def game_move(self, event):
        await self.send(text_data=json.dumps(
            {
                'type': 'websocket.render',
                'border_to_render': event['border_to_render']
            }
        ))
