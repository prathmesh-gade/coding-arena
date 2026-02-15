import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer

rooms={}

class BattleConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room=self.scope["url_route"]["kwargs"]["room"]
        self.group=f"room_{self.room}"

        await self.channel_layer.group_add(self.group,self.channel_name)

        await self.accept()

        color=f"#{random.randint(0,0xFFFFFF):06x}"

        if self.room not in rooms:
            rooms[self.room]=[]

        rooms[self.room].append(color)

        await self.send_presence()

    async def disconnect(self,close_code):

        if self.room in rooms:
            rooms[self.room].pop()

        await self.channel_layer.group_discard(self.group,self.channel_name)

        await self.send_presence()

    async def send_presence(self):

        await self.channel_layer.group_send(
            self.group,
            {
                "type":"presence_event",
                "users":rooms[self.room]
            }
        )

    async def presence_event(self,event):

        await self.send(text_data=json.dumps({
            "type":"presence",
            "users":event["users"]
        }))

    async def receive(self,text_data):

        data=json.loads(text_data)

        if data["type"]=="code":

            await self.channel_layer.group_send(
                self.group,
                {
                    "type":"code_event",
                    "file":data["file"],
                    "code":data["code"]
                }
            )

        if data["type"]=="file_create":

            await self.channel_layer.group_send(
                self.group,
                {
                    "type":"file_create_event",
                    "file":data["file"]
                }
            )

        if data["type"]=="file_switch":

            await self.channel_layer.group_send(
                self.group,
                {
                    "type":"file_switch_event",
                    "file":data["file"]
                }
            )

    async def code_event(self,event):

        await self.send(text_data=json.dumps({
            "type":"code",
            "file":event["file"],
            "code":event["code"]
        }))

    async def file_create_event(self,event):

        await self.send(text_data=json.dumps({
            "type":"file_create",
            "file":event["file"]
        }))

    async def file_switch_event(self,event):

        await self.send(text_data=json.dumps({
            "type":"file_switch",
            "file":event["file"]
        }))
