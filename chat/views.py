from django.shortcuts import render
from django.http import HttpResponse


def chat(request):
    return render(request, 'chat/chat.html')
