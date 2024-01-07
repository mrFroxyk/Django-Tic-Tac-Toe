from django.urls import path
from .views import chat

app_name = "chat"
urlpatterns = [
    path('', chat, name='chat')
]
