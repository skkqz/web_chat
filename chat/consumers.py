import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import MessageChatModel, RoomChatModel
from accounts.models import ProfileUserModel

User = get_user_model()


class PersonalChatConsumer(AsyncWebsocketConsumer):
    """
    Отправка и получение сообщений в чате
    """

    async def connect(self):
        my_id = self.scope['user'].id
        other_user_id = self.scope['url_route']['kwargs']['id']

        if int(my_id) > int(other_user_id):
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            self.room_name = f'{other_user_id}-{my_id}'

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )  # Добавляем текущее соединение к группе комнаты

        await self.accept()  # Принимаем WebSocket-соединение

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)  # Распаковываем JSON-данные из текстового сообщения
        message = data['message']  # Извлекаем сообщение из данных
        username = data['username']  # Извлекаем имя пользователя из данных
        receiver = data['receiver']  # Извлекаем получателя сообщения из данных

        await self.save_message(self.scope['user'].id, self.room_group_name,
                                message)  # Сохраняем сообщение в базе данных

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )  # Отправляем сообщение всем участникам комнаты

    async def chat_message(self, event):
        message = event['message']  # Извлекаем сообщение из события
        username = event['username']  # Извлекаем имя пользователя из события

        await self.send(text_data=json.dumps({
            'message': message,  # Отправляем сообщение обратно клиенту
            'username': username,
            'room': self.room_group_name
        }))

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )  # Удаляем текущее соединение из группы комнаты при разрыве

    @database_sync_to_async
    def save_message(self, user_id, thread_name, message):

        profile = ProfileUserModel.objects.get(user=user_id)
        room = RoomChatModel.objects.get(name=thread_name)

        MessageChatModel.objects.create(
            sender=profile,
            message=message,
            room_name=room,
        )

        # other_user_id = self.scope['url_router']['kwargs']['id']
        # get_user = User.objects.get(id=other_user_id)
        # if receiver == get_user.username:
        #     ChatNotification.objects.create(chat=chat_obj, user=get_user)


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    """
    Определения статуса пользователя Online or Offline
    """

    async def connect(self):
        self.room_group_name = 'user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        username = data['username']
        connection_type = data['type']

        print(data)

        await self.change_online_status(username, connection_type)

    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']
        await self.send(text_data=json.dumps({
            'username': username,
            'online_status': online_status
        }))

    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def change_online_status(self, username, c_type):
        user = User.objects.get(username=username)
        userprofile = ProfileUserModel.objects.get(user=user)
        if c_type == 'open':
            userprofile.online_status = True
            userprofile.save()
        else:
            userprofile.online_status = False
            userprofile.save()
