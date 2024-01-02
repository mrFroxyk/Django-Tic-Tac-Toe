from channels.consumer import AsyncConsumer


class SimpleMessageConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept',
            'message': 'Hello from django server',
        })
        print("connect", event)

    async def websocket_receive(self, text_data):
        await self.send({
            'type': 'websocket.send',
            'text': 'Hello from django server',
        })
        print("message!", text_data)

    async def websocket_disconnect(self):
        pass
