from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import views

queue = []


class Queue(views.APIView):
    """
    Queue manager. Players who are searching for a game
    arrive here and wait to create the game
    """
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
        """
        Request to create a new game lobby. If there are enough users in the
        queue to create a game (2 users), their channel names will be returned.
        """
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
        """
        If a user disconnects from the queue, they will be deleted from the list
        """
        global queue
        user_code = request.query_params.get('user_code')
        try:
            queue.remove(user_code)
        except ValueError:
            ...
        return Response(status=status.HTTP_200_OK)
