import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .serializers import MessageSerializer
class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_message(self,username,message):
        data = {'username':username,'message':message}
        print(data)
        message = MessageSerializer(data=data)
        if message.is_valid():
            message.save()
            return message.data
        else:
            print(message.error_messages)
            return False

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        print(f"Connecting to room: {self.room_name}")
        print(self.channel_name)
        self.roomGroupName = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )   
        print(f"Connecting to room: {self.roomGroupName}")
        await self.accept()
    
    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName , 
            self.channel_name 
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        
        data = await self.get_message(username,message)
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type" : "sendMessage" ,
                "message":data
                
            })
        
        
    async def sendMessage(self , event) : 
        
        message = event['message']
        print(message)
        if message:
            await self.send(json.dumps(message))
        else:
            await self.send(json.dumps({'value':False}))
    
    