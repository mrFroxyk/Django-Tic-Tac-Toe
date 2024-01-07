# from channels.consumer import AsyncConsumer
#
#
# class OnlineUser(AsyncConsumer):
#     async def websocket_connect(self, event):
#         await self.send({
#             'type': 'websocket.accept',
#             'msg': 'connect',
#         })
#
#     async def websocket_receive(self, data):
#         print(data)
#         await self.send({
#             'type': 'websocket.send',
#             'msg': 'receive'
#         })


