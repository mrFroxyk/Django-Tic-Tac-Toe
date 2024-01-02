from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        "Tittle": "test web socket"
    }
    return render(request, "message_test/socket.html")
