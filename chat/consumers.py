import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

# from .models import ChatModel, UserProfileModel


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope['user'].id  # Получаем идентификатор текущего пользователя из атрибута 'user' в scope
        other_user_id = self.scope['url_route']['kwargs']['id']  # Получаем идентификатор другого пользователя из URL-параметров

        print(f'my_id: {my_id} // id_user: {other_user_id}')

        if int(my_id) > int(other_user_id):  # Сравниваем идентификаторы, чтобы создать уникальное имя комнаты
            self.room_name = f'{my_id}-{other_user_id}'  # Формируем имя комнаты
        else:
            self.room_name = f'{other_user_id}-{my_id}'  # Формируем имя комнаты

        self.room_group_name = 'chat_%s' % self.room_name  # Формируем имя группы для WebSocket-комнаты

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )  # Добавляем текущее соединение к группе комнаты

        await self.accept()  # Принимаем WebSocket-соединение

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)  # Распаковываем JSON-данные из текстового сообщения
        print(data)  # Выводим данные в консоль
        message = data['message']  # Извлекаем сообщение из данных
        username = data['username']  # Извлекаем имя пользователя из данных
        receiver = data['receiver']  # Извлекаем получателя сообщения из данных

        # await self.save_message(username, self.room_group_name, message, receiver)  # Сохраняем сообщение в базе данных

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # Отправляем событие типа 'chat_message'
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