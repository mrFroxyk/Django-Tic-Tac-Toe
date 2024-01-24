from django.urls import path
from .views import chat
from .consumers import ChatConsumer

app_name = "chat"
urlpatterns = [
    path('', chat, name='chat')
]

websocket_urlpatterns_chat = [
    path('chat', ChatConsumer.as_asgi(), name='chat')
]
