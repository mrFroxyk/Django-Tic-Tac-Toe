import time

from channels.layers import get_channel_layer
from django.core.cache import cache
import random
import asyncio


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
    # asyncio.create_task(check_game_end(120, room_code=room_code))
    return


channel_layer = get_channel_layer()


async def check_game_end(second: int, room_code: str):
    await asyncio.sleep(second)
    room_data = cache.get(room_code)
    room_data['is_end'] = True
    room_data['status'] = 'Time is over'
    # Correct the time of move if a connection occurs between moves
    time_delta = int(time.time()) - room_data['time_last_action']
    match room_data['current_player']:
        case 'player1':
            room_data['player1_time'] -= time_delta
        case 'player2':
            room_data['player2_time'] -= time_delta
    await channel_layer.group_send(
        room_code, room_data
    )

    await channel_layer.group_send(
        room_code,
        {
            'type': 'game.end'
        }
    )
    cache.set(room_code, room_data)
