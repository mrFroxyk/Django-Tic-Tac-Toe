import random

from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from django.http import HttpResponse
from chat.views import chat
import secrets


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
    # room_code = secrets.token_hex(8)
    room_code = 'aboba'
    cache.set(
        room_code, {
            'player1': request.user.username,
            'player2': None,
            'current_move': 'X',
            'current_player': random.choice(['player1', 'player2']),
            'border_to_render': [''] * 9,
            'is_end': False,
            'is_start': False,
        }
    )
    return redirect(reverse('game_lobby', kwargs={'room_code': room_code}))


def game_lobby(request, room_code):
    context = {}
    return render(request, 'game/game_lobby.html', context)
    # return HttpResponse(f"It's a {room_code} room")


def game(request, room_code):
    # TODO: check for game end
    chat_template = chat(request)
    chat_template.render()
    context = {
        'chat': chat_template.rendered_content,
        'request': request
    }
    return render(request, 'game/game.html', context)
