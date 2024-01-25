from django.shortcuts import render
from django.template.response import TemplateResponse


# def chat(request):
#     return render(request, 'chat/chat.html')

def chat(request):
    return TemplateResponse(request, 'chat/chat.html', {})
