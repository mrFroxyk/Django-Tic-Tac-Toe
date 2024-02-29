from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response


class Queue(views.APIView):
    def post(self, request):
        print('nice')
        data = {
            'ms': 'test'
        }
        return Response(data)
    def get(self, request):
        print('nice')
        data = {
            'ms': 'test'
        }
        return Response(data)
