from django.urls import path
from .views import game_lobby, create_game, game
from .consumers import GameManagerConsumer

urlpatterns = [
    path('', game_lobby, name='game_lobby'),
    path('create_game', create_game, name='create_game'),
    path('<str:room_code>', game, name='game')
]

websocket_urlpatterns_game = [
    path('game', GameManagerConsumer.as_asgi(), name='game')
]
