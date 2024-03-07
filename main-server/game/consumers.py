import random
import secrets

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from urllib.parse import parse_qs
from django.urls import reverse
import asyncio
import json
import time
import httpx

from .game_logic import *


class GameLobby(AsyncWebsocketConsumer):
    """
    Consumer for the game lobby. The user is redirected here from
    game_create view and will be redirected to game (play) when
    he finds an opponent
    """

    async def connect(self):
        query_params = parse_qs(self.scope['query_string'].decode('utf-8'))
        room_code = query_params.get('room_code', [None])[0]
        if not room_code:
            await self.close(code=400)
        else:
            room_data = cache.get(room_code)
            current_username = self.scope['user'].username
            if current_username == room_data['player1']:
                await self.channel_layer.group_add(
                    room_code,
                    self.channel_name
                )

                await self.channel_layer.group_send(
                    room_code,
                    {
                        'type': 'lobby.message',
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
                        'type': 'lobby.message',
                        'message': 'second connected'
                    }
                )
                room_data['player2'] = self.scope['user'].username
                await self.channel_layer.group_send(
                    room_code,
                    {
                        'type': 'lobby.redirect',
                        'relative_url': reverse('game:game', kwargs={'room_code': room_code})
                    }
                )
                room_data['time_last_action'] = int(time.time())

                current_player_nick = room_data[room_data['current_player']]
                room_data['is_start'] = True
                room_data['status'] = f'{current_player_nick} (X) is moving now'

                cache.set(room_code, room_data)
            await self.accept()

    async def lobby_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'websocket.message',
            'message': event['message']
        }))

    async def lobby_redirect(self, event):
        await self.send(text_data=json.dumps(event))


class Game(AsyncWebsocketConsumer):
    """
    Consumer for game
    """

    def __init__(self):
        super().__init__()

    async def connect(self):
        """
        Accept connections from requests with the template
        'ws://host:8000/game?room_code=room_code',
        either as an observer or a gamer.
        """
        query_params = parse_qs(self.scope['query_string'].decode('utf-8'))
        room_code = query_params.get('room_code', [''])[0]
        if room_code:
            # asyncio.create_task(self.check_end(1 + 2, room_code))
            await self.accept()
        else:
            await self.close(code=400)
            return

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

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            room_code = response['room_code']
            match response['type']:
                case 'move':
                    move_id = int(response['position'])
                    username = self.scope['user'].username
                    room_data = make_move(room_code, move_id, username)
                    if check_winner(room_data, username):
                        status = check_winner(room_data, username)
                        room_data = end_game(room_code, room_data, status)
                        await self.channel_layer.group_send(
                            room_code, room_data
                        )
                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'game.end'
                            }
                        )
                        return
                    await self.channel_layer.group_send(
                        room_code, room_data
                    )

                case 'revenge_request':
                    username = self.scope['user'].username

                    rematch_response = rematch_request(room_code, username)
                    room_data = rematch_response.room_data

                    if rematch_response.accept_rematch:
                        # If both players agree, start a rematch.
                        old_room_code_count = int(room_code.split('.')[1])  # 'fjord12.2' -> 2
                        old_room_code_body = room_code.split('.')[0]  # 'fjord12.2' -> fjord12
                        new_room_code = old_room_code_body + '.' + str(old_room_code_count + 1)

                        create_new_game(
                            room_code=new_room_code,
                            player1=room_data['player1'],
                            player2=room_data['player2'],
                            is_start=True,
                            time_last_action=int(time.time()),
                            set_game_status=True,
                        )

                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'game.redirect',
                                'relative_url': reverse('game:game', kwargs={'room_code': new_room_code})
                            }
                        )
                    else:
                        # Send an invitation to a rematch to the opponent.
                        await self.channel_layer.group_send(
                            room_code,
                            {
                                'type': 'game.revenge'
                            }
                        )

    async def disconnect(self, code):
        ...

    async def game_move(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_end(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_revenge(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_redirect(self, event):
        await self.send(text_data=json.dumps(event))


class SearchGame(AsyncWebsocketConsumer):
    async def connect(self):
        # Adding a user to the queue for waiting for opponent
        cache.set(
            self.channel_name,
            self.scope['user'].username
        )
        async with httpx.AsyncClient() as client:
            data = {
                'user_code': self.channel_name
            }
            response_to_send_new_user = await client.post('http://127.0.0.1:8001/queue', data=data)

            if response_to_send_new_user.status_code == 202:
                # Attempt to create a new game
                response_to_create_queue = await client.get('http://127.0.0.1:8001/queue')
                if response_to_create_queue.status_code == 200:
                    user_codes = json.loads(response_to_create_queue.text).get('user_codes')
                    current_room_code = str(secrets.token_hex(8)) + '.' + '0'
                    create_new_game(
                        room_code=current_room_code,
                        player1=cache.get(user_codes[0]),
                        player2=cache.get(user_codes[1]),
                        is_start=True,
                        time_last_action=int(time.time()),
                        set_game_status=True,
                    )
                    for channel_name_code in user_codes:
                        await self.channel_layer.send(
                            channel_name_code,
                            {
                                'type': 'search.redirect',
                                'relative_url': reverse('game:game', kwargs={'room_code': current_room_code})
                            }
                        )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            print(response)

    async def disconnect(self, code):
        async with httpx.AsyncClient() as client:
            data = {
                'user_code': self.channel_name
            }
            await client.delete('http://127.0.0.1:8001/queue', params=data)

    async def search_redirect(self, event):
        await self.send(text_data=json.dumps(event))
