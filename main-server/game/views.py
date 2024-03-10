from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from chat.views import chat
from .game_logic import create_new_game
import secrets
import random

from Core.celery import check_game_end, print_ms


def find_game(request):
    print_ms.delay()
    chat_template = chat(request)
    chat_template.render()
    context = {
        'chat': chat_template.rendered_content,
        'user': request.user,
    }
    return render(request, 'game/findGame.html', context)


def create_game(request):
    """
    Middle function, who create game session in the cache and
    redirected user to '/game/{room_code}/game'. He waits for second player after
    the game there
    """
    room_code = str(secrets.token_hex(8)) + '.' + '0'
    # room_code = 'aboba'
    create_new_game(
        room_code=room_code,
        player1=request.user.username,
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
        'random_number': random_number,
        'user': request.user,
    }
    return render(request, 'game/gameLobby.html', context)


def game(request, room_code):
    # TODO: check for game end
    chat_template = chat(request)
    room_data = cache.get(room_code)
    random_number = random.randint(1, 100)
    chat_template.render()
    context = {
        'chat': chat_template.rendered_content,
        'request': request,
        'random_number': random_number,
        'user': request.user,
        'player1': room_data['player1'],
        'player2': room_data['player2'],
    }
    return render(request, 'game/gameWithFriend.html', context)


def local_game(request):
    random_number = random.randint(1, 100)
    context = {
        'request': request,
        'random_number': random_number,
        'user': request.user,
        'player1': 'player1',
        'player2': 'player2',
    }
    return render(request, 'game/localGame.html', context)


def game_with_bot(request):
    random_number = random.randint(1, 100)
    context = {
        'request': request,
        'random_number': random_number,
        'user': request.user,
        'player1': request.user,
        'player2': 'bot',
    }
    return render(request, 'game/gameWithBot.html', context)
