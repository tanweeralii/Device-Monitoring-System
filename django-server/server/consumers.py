import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
        
class SocketConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        self.room_name = self.scope['url_route']['kwargs']['host_name']
        print(self.room_name)
        self.room_group_name = 'pair_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    async def websocket_disconnect(self, event):
        print("disconnect", event)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def websocket_receive(self, event):
        print(event)
        print(event["text"])
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "tester_message",
            "text": event["text"],
        })
        
    async def tester_message(self, event):
        text = event["text"]
        await self.send(text)
