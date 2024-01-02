from .consumers import SimpleMessageConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws', SimpleMessageConsumer.as_asgi(), name="ws")
]
