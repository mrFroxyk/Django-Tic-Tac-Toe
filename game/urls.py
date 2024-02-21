from django.urls import path
from .views import *
from .consumers import GameLobby, Game

app_name = 'game'
urlpatterns = [
    path('', create_game, name='create_game'),
    path('<str:room_code>/lobby', game_lobby, name='game_lobby'),
    path('<str:room_code>/game', game, name='game'),
    path('local-game', local_game, name='local_game'),
    path('game-with-bot', game_with_bot, name='game_with_bot'),
]

websocket_urlpatterns_game = [
    path('game_lobby', GameLobby.as_asgi(), name='ws_game_lobby'),
    path('game', Game.as_asgi(), name='ws_game'),
]
