from django.shortcuts import render, redirect, reverse
from django.core.cache import cache
from django.http import HttpResponse
from chat.views import chat
import secrets


def game_lobby(request):
    chat_template = chat(request)
    chat_template.render()
    context = {
        'chat': chat_template.rendered_content
    }
    return render(request, 'game/game_lobby.html', context)


def create_game(request):
    """
    Middle function, who create game session in the cache and
    redirected user to '/game/{room_code}'. He waits for second player after
    the game there
    """
    room_code = secrets.token_hex(8)


    cache.set(
        room_code, {
            'player1': request.user.username,
            'player2': None,
            'moves': '',
            'is_end': False
        }
    )
    return redirect(reverse('game', kwargs={'room_code': room_code}))


def game(request, room_code):

    # chat_template = chat(request)
    # chat_template.render()
    # context = {
    #     'chat': chat_template.rendered_content
    # }
    context = {}
    return render(request, 'game/game.html', context)
    # return HttpResponse(f"It's a {room_code} room")
