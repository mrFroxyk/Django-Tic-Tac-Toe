from django.urls import path
from .consumers import OnlineUser
from .views import *

websocket_urlpatterns_online_user = [
    path('online', OnlineUser.as_asgi(), name='online')
]

urlpatterns = [
    path('', online, name='online')
]
