import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import ChatMessage
from .services import ChatProjectAccessMixin, addProjectChatMessage

# Проверка доступа пользователя к чату проекта и добавления нового пользователя в группу чата проекта
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user_id = self.scope['user'].id
        project_id = int(self.scope['url_route']['kwargs']['project_id'])
        
        if ChatProjectAccessMixin(user_id, project_id).checkAccess():
            self.room_group_name = f'project_chat_{project_id}'
            
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name)
            self.accept()

# Этот код удаляет пользователя из группы каналов для данной комнаты. Это позволяет системе не отправлять сообщения дисконнектированным пользователям.

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name)

# Этот код реализует прием сообщения чат и отправку этого сообщения в группу чата. 
# Он берет данные сообщения из аргумента text_data, десериализует их и добавляет в базу данных сообщений чата.
# Затем он отправляет сообщение в цепочку комнаты,   используя метод async_to_sync, с содержанием сообщения, отправителя и изображения отправителя
# Таким образом, данный код позволяет добавлять и отправлять сообщения в группу чата.

    def receive(self, text_data):
        message_data= json.loads(text_data)
        
        chat_message_or_errors = addProjectChatMessage(
            message_data['message'], message_data['sender'],
            self.scope['url_route']['kwargs']['project_id']
        )
        if isinstance(chat_message_or_errors, ChatMessage):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': chat_message_or_errors.message,
                    'sender': chat_message_or_errors.sender.id,
                    'sender_image': chat_message_or_errors.sender.image.url
                },
            )

# отправляет сообщение в чат в виде json-документа, указав его содержание, изображение отправителя и тип сообщения. 
# также проверяет, отправитель сообщения является ли самим пользователем, и если это так, то добавляет тип сообщения 'myMessage'.

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': event.get('message'), 
            'sender_image': event.get('sender_image'),
            'message_type': 'myMessage' if self.scope['user'].id == event.get('sender') else ''
        }))
