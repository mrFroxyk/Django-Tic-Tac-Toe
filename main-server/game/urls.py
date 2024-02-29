from django.urls import path
from .views import *
from .consumers import *

app_name = 'game'
urlpatterns = [
    path('', create_game, name='create_game'),
    path('<str:room_code>/lobby', game_lobby, name='game_lobby'),
    path('<str:room_code>/game', game, name='game'),
    path('local-game', local_game, name='local_game'),
    path('fast-game', find_game, name='fast_game')

]

websocket_urlpatterns_game = [
    path('game_lobby', GameLobby.as_asgi(), name='ws_game_lobby'),
    path('game', Game.as_asgi(), name='ws_game'),
    path('fast-game', FastGame.as_asgi(), name='ws_fast_game'),
]
