from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from colors.models import OrderHistory,User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # You can use a fixed group name for the Raspberry Pi
        self.raspberry_pi_group_name = "raspberry_pi"

        # Join the Raspberry Pi group
        await self.channel_layer.group_add(
            self.raspberry_pi_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the Raspberry Pi group
        await self.channel_layer.group_discard(
            self.raspberry_pi_group_name,
            self.channel_name
        )
    
    @database_sync_to_async
    def confirm_order(self,text_data_json):
        if "status" in text_data_json:
            if text_data_json['status'] == "success":
                if "userid" in text_data_json.keys() and "orderid" in text_data_json.keys():
                    userid = text_data_json['userid']
                    orderid = text_data_json['orderid']
                    user = User.objects.get(id=userid)
                    orderhistory = OrderHistory.objects.get(id=orderid,user=user)
                    orderhistory.status = OrderHistory.Status.ORDER_CONFIRMED
                    red = orderhistory.red
                    blue = orderhistory.blue
                    yellow = orderhistory.yellow
                    green = orderhistory.green
                    if red:
                        # print("red ",red)
                        count = getattr(user, "red")
                        if not (count - red < 0):
                            setattr(user, "red", count - red)
                        else:
                            orderhistory.status = None
                            orderhistory.error = "You don't have enough 'Red' to complete the order"
                            orderhistory.is_error = True
                    if blue:
                        # print("blue ",blue)
                        count = getattr(user, "blue")
                        if not (count - blue < 0):
                            setattr(user, "blue", count - blue)
                        else:
                            orderhistory.status = None
                            orderhistory.error = "You don't have enough 'Blue' to complete the order"
                            orderhistory.is_error = True
                    if yellow:
                        # print("yellow ",yellow)
                        count = getattr(user, "yellow")
                        if not (count - yellow < 0):
                            setattr(user, "yellow", count - yellow)
                        else:
                            orderhistory.status = None
                            orderhistory.error = "You don't have enough 'Yellow' to complete the order"
                            orderhistory.is_error = True
                    if green:
                        # print("green ",green)
                        count = getattr(user, "green")
                        if not (count - green < 0):
                            setattr(user, "green", count - green)
                        else:
                            orderhistory.status = None
                            orderhistory.error = "You don't have enough 'Green' to complete the order"
                            orderhistory.is_error = True
                    user.save()
                    orderhistory.save()
                    print("Order confimred and updated")
            elif text_data_json['status'] == "error":
                if "userid" in text_data_json.keys() and "orderid" in text_data_json.keys():
                    userid = text_data_json['userid']
                    orderid = text_data_json['orderid']
                    orderhistory = OrderHistory.objects.get(id=orderid,user=user)
                    orderhistory.status = OrderHistory.Status.ORDER_CONFIRMED
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.confirm_order(text_data_json)
        # if "status" in text_data_json:
        #     if text_data_json['status'] == "success":
        #         if "userid" in text_data_json.keys() and "orderid" in text_data_json.keys():
        #             userid = text_data_json['userid']
        #             orderid = text_data_json['orderid']
        #             user = User.objects.get(id=userid)
        #             orderhistory = OrderHistory.objects.get(id=orderid,user=user)
        #             print(orderhistory)
        #     elif text_data_json['status'] == "error":
        #         if "userid" in text_data_json.keys() and "orderid" in text_data_json.keys():
        #             userid = text_data_json['userid']
        #             orderid = text_data_json['orderid']
        # message = text_data_json["message"]

        # Send the message to the Raspberry Pi group
        # await self.channel_layer.group_send(
        #     self.raspberry_pi_group_name,
        #     {
        #         "type": "raspberry_pi.message",
        #         "message": message,
        #     }
        # )

    async def raspberry_pi_message(self, event):
        message = event["message"]
        print(event)
        # Send the message to the WebSocket (Raspberry Pi)
        await self.send(text_data=json.dumps({"message": message}))
