from django.shortcuts import render
from django.http import HttpResponse
from channels.layers import get_channel_layer


# Create your views here.
def online(request):
    channel_layer = get_channel_layer()

    print(request.user.is_authenticated)
    print(request.session['guest_id'])
    return HttpResponse("test")
