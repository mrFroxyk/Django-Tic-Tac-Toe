from django.urls import path
from .consumers import OnlineUser

websocket_urlpatterns_online_user = [
    path('online', OnlineUser.as_asgi(), name='online')
]
