from channels.layers import get_channel_layer
from django.core.cache import cache
from enum import Enum
import asyncio
import random
import time
from Core.celery import check_game_end, print_ms


def create_new_game(
        room_code: str,
        type: str = 'game.move',
        player1: str = None,
        player2: str = None,
        current_move: str = 'X',
        border_to_render: list = [''] * 9,
        status: str = 'Wait for game',
        is_end: bool = False,
        is_start: bool = False,
        player1_time: int = 120,
        player2_time: int = 120,
        player1_rematch_request: bool = False,
        player2_rematch_request: bool = False,
        time_last_action: int = 0,

        set_game_status: bool = False,
) -> None:
    """
    :param room_code: The generated room code must be unique
    :param type: Type for game consumer (usually game.move)
    :param player1: First player nick's
    :param player2: Second player nick's
    :param current_move: Current move (X or O)
    :param border_to_render: Current border state. Example: ['X', '', 'X', 'O', 'X', 'O', 'X', 'O', ''] is meaning
                                                            X . X
                                                            O X O
                                                            X O .
    :param status: Current game status. Example: admin (X) is moving / Wait for game / ...
    :param is_end: A boolean state indicating whether the game is over
    :param is_start: A boolean state indicating whether the game start
    :param player1_time: Remaining time for 1 player moves
    :param player2_time: Remaining time for 2 player moves
    :param player1_rematch_request: The boolean state indicates that 1 player agrees to a rematch.
    :param player2_rematch_request: The boolean state indicates that 2 player agrees to a rematch.
    :param time_last_action: Unix time last move
    :param set_game_status: Boolean param rewrite default status on '{Player}(X) is moving'
    :return: Nothing return. Write game state in cache (redis)
    """
    room_data = {
        'type': type,
        'room_code': room_code,
        'player1': player1,
        'player2': player2,
        'current_move': current_move,
        'current_player': random.choice(['player1', 'player2']),
        'border_to_render': border_to_render,
        'status': status,
        'is_end': is_end,
        'is_start': is_start,
        'player1_time': player1_time,
        'player2_time': player2_time,
        'player1_rematch_request': player1_rematch_request,
        'player2_rematch_request': player2_rematch_request,
        'time_last_action': time_last_action,
    }

    if set_game_status:
        room_data['status'] = f"{room_data[room_data['current_player']]} (X) is moving",

    cache.set(
        room_code,
        room_data,
    )
    # print_ms.delay()
    # asyncio.create_task(check_game_end(120, room_code=room_code))
    # check_game_end
    # task = check_game_end.apply_async(args=[room_code], countdown=2)

    return


channel_layer = get_channel_layer()


def make_move(room_code, move_id, username):
    room_data = cache.get(room_code)

    if (username != room_data[room_data['current_player']]) or (room_data['is_end']) or not (
            room_data['is_start']):
        return room_data

    if username == room_data['player1']:
        enemy_user_num = 'player2'
    if username == room_data['player2']:
        enemy_user_num = 'player1'

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

        if current_move == 'X':
            current_move = 'O'
        else:
            current_move = 'X'

        enemy_user_nick = room_data[enemy_user_num]
        room_data['status'] = f'{enemy_user_nick} ({current_move}) is moving now'
        response = room_data

        room_data['current_move'] = current_move
        room_data['border_to_render'] = border_to_render

        cache.set(room_code, room_data)

        return response


def end_game(room_code, room_data, status):
    room_data['status'] = status
    room_data['is_end'] = True
    cache.set(room_code, room_data)
    return room_data


def check_winner(room_data, current_player):
    border = room_data['border_to_render']
    win_position = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for (i1, i2, i3) in win_position:
        if border[i1] == border[i2] == border[i3] and border[i1] != '':
            return f'{current_player} ({border[i1]}) is win! Congratulation!'


class RematchResponse:
    def __init__(self, accept_rematch, room_data):
        self.accept_rematch = accept_rematch
        self.room_data = room_data


def rematch_request(room_code, username):
    room_data = cache.get(room_code)
    if username == room_data['player1']:
        room_data['player1_rematch_request'] = True
    if username == room_data['player2']:
        room_data['player2_rematch_request'] = True
    cache.set(room_code, room_data)

    if room_data['player1_rematch_request'] == room_data['player2_rematch_request'] == True:
        accept_rematch = True
    else:
        accept_rematch = False

    return RematchResponse(accept_rematch, room_data)
