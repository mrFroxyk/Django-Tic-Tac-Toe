from django.urls import path
from .views import find_game, create_game, game_lobby, game
from .consumers import GameLobby

urlpatterns = [
    path('', find_game, name='find_game'),
    path('create_game', create_game, name='create_game'),
    path('<str:room_code>/lobby', game_lobby, name='game_lobby'),
    path('<str:room_code>/game', game, name='game'),
]

websocket_urlpatterns_game = [
    path('game', GameLobby.as_asgi(), name='game')
]
