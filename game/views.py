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

    game_type = request.GET.get('game_type', None)
    if not game_type:
        raise Http404("Запрашиваемая страница не найдена")

    room_data = {
        'type': 'game.move',
        'room_code': '',
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
    # room_code = 'aboba'
    match game_type:
        case 'new_game':
            room_code = str(secrets.token_hex(8)) + '.' + '0'
            room_data['room_code'] = room_code
            cache.set(
                room_code, room_data
            )
            return redirect(reverse('game:game_lobby', kwargs={'room_code': room_code}))

        case 'revenge':
            old_room_code = request.GET.get('old_room_code', None)
            if old_room_code:
                old_room_code_count = int(old_room_code.split('.')[1])  # 'fjord12/2' -> 2
                old_room_code_body = old_room_code.split('.')[0]  # 'fjord12/2' -> fjord12
                room_code = old_room_code_body + str(old_room_code_count + 1)

                room_code = str(secrets.token_hex(8)) + '.' + '0'
                room_data['room_code'] = room_code
                cache.set(
                    room_code, room_data
                )

                return redirect(reverse('game:game_lobby', kwargs={'room_code': room_code}))
            else:
                return HttpResponseBadRequest

        case _:
            return HttpResponseBadRequest


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
