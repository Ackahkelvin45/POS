from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
        def connect(self):
            print(self.channel_name)
            self.accept()
            self.GROUP_NAME='user-notifications'
            async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
             )
        def disconnect(self, close_code):
           async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME, self.channel_name
        )
        def pharmacy_verified(self, event):
            self.send(text_data=event['text'])