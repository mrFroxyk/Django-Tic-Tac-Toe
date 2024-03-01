from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import views

queue = []


class Queue(views.APIView):
    @staticmethod
    def post(request: Request):
        global queue
        """
        Accept data to place the user in the queue
        """
        data = request.data
        user_code = data.get('user_code')
        if user_code:
            queue.append(user_code)
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request: Request):
        global queue
        if len(queue) >= 2:
            user_to_redirect = queue[:2]
            queue = queue[2:]
            data = {
                'user_codes': user_to_redirect,
            }
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request: Request):
        global queue
        user_code = request.query_params.get('user_code')
        queue.remove(user_code)
        return Response(status=status.HTTP_200_OK)
