
class GameManagerConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            response = json.loads(text_data)
            match response['type']:
                case 'join':
                    current_username = self.scope['user'].username
                    room_code = response['room_code']
                    room_data = cache.get(room_code)

                    if current_username == room_data['player1']:
                        print(room_code, self.channel_name)
                        self.channel_layer.group_add(
                            room_code,
                            self.channel_name
                        )
                        print('типа начал рассылку')
                        await self.channel_layer.group_send(
                            room_code,
                            {'type': 'game.message', 'message': '123'}
                        )
                    elif not room_data['player2']:
                        print(room_code)
                        self.channel_layer.group_add(
                            room_code,
                            self.channel_name
                        )
                        print('типа начал рассылку')
                        await self.channel_layer.group_send(
                            room_code,
                            {'type': 'chat.message', 'message': '123'}
                        )
                        room_data['player2'] = current_username
                        cache.set(room_code, room_data)
                        # now game data is
                        # {'player1': 'guest_15', 'player2': 'guest_16', 'moves': '', 'is_end': False}
                        # format
                case 'move':
                    ...

    async def disconnect(self, code):
        print("disconnect")

    async def chat_message(self, event):
        print(event)
        print("tARGET")
        await self.send(text_data=json.dumps({
            'type': 'websocket.message',
            'message': event['message']
        }))