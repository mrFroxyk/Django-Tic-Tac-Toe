from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
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

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.enemy_user_num = None
        self.username = None
        self.user_num = None
        self.room_code = None

    async def connect(self):
        self.username = self.scope['user'].username
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            print(response)
            match response['type']:
                case 'join':
                    self.room_code = response['room_code']
                    await self.channel_layer.group_add(
                        self.room_code,
                        self.channel_name
                    )
                    room_data = cache.get(self.room_code)
                    if self.username == room_data['player1']:
                        self.user_num = 'player1'
                        self.enemy_user_num = 'player2'
                    elif self.username == room_data['player2']:
                        self.user_num = 'player2'
                        self.enemy_user_num = 'player1'

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
                    room_data = cache.get(self.room_code)

                    if self.user_num != room_data['current_player']:
                        return
                    move_id = int(response['position'])
                    border_to_render = room_data['border_to_render']
                    current_move = room_data['current_move']
                    if border_to_render[move_id] == '':
                        border_to_render[move_id] = current_move
                        room_data['current_player'] = self.enemy_user_num
                        current_time = int(time.time())
                        time_delta = int(time.time()) - room_data['time_last_action']
                        room_data['time_last_action'] = int(time.time())
                        match room_data['current_player']:
                            case 'player1':
                                room_data['player2_time'] -= time_delta
                            case 'player2':
                                room_data['player1_time'] -= time_delta

                        await self.channel_layer.group_send(
                            self.room_code, room_data
                        )
                        if current_move == 'X':
                            current_move = 'O'
                        else:
                            current_move = 'X'

                        room_data['current_move'] = current_move
                        room_data['border_to_render'] = border_to_render
                        cache.set(self.room_code, room_data)

    async def disconnect(self, code):
        ...

    async def game_move(self, event):
        event['type'] = 'websocket.render'
        await self.send(text_data=json.dumps(event))
