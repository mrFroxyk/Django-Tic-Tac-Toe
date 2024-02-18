import time

from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from chat.views import chat
from django.http import Http404, HttpResponseBadRequest
import secrets
import random


def find_game(request):
    chat_template = chat(request)
    chat_template.render()
    context = {
        'chat': chat_template.rendered_content
    }
    return render(request, 'game/find_game.html', context)


def create_game(request):
    """
    Middle function, who create game session in the cache and
    redirected user to '/game/{room_code}/game'. He waits for second player after
    the game there
    """
    room_code = str(secrets.token_hex(8)) + '.' + '0'
    # room_code = 'aboba'

    room_data = {
        'type': 'game.move',
        'room_code': room_code,
        'player1': request.user.username,
        'player2': None,
        'current_move': 'X',
        'current_player': random.choice(['player1', 'player2']),
        'border_to_render': [''] * 9,
        'status': 'Wait for game',
        'is_end': False,
        'is_start': False,
        'player1_time': 120,
        'player2_time': 120,
        'player1_rematch_request': False,
        'player2_rematch_request': False,
        'time_last_action': 0,
    }

    cache.set(
        room_code, room_data
    )
    return redirect(reverse('game:game_lobby', kwargs={'room_code': room_code}))


def game_lobby(request, room_code):
    # TODO: integrate chat in structure
    chat_template = chat(request)
    chat_template.render()
    random_number = random.randint(1, 100)
    context = {
        'chat': chat_template.rendered_content,
        'request': request,
        'url': request.build_absolute_uri(),
        'random_number': random_number
    }
    return render(request, 'game/game_lobby.html', context)


def game(request, room_code):
    # TODO: check for game end
    chat_template = chat(request)
    random_number = random.randint(1, 100)
    chat_template.render()
    context = {
        'chat': chat_template.rendered_content,
        'request': request,
        'random_number': random_number
    }
    return render(request, 'game/game.html', context)
