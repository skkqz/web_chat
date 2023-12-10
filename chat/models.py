from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import ProfileUserModel

User = get_user_model()


class RoomChatModel(models.Model):
    """
    Модель комнаты чата
    """

    name = models.CharField(max_length=100, verbose_name='Комната чата')
    user_first = models.ForeignKey(ProfileUserModel, on_delete=models.CASCADE, blank=True,
                                   null=True, verbose_name='Первый пользователь', related_name='user_1')
    user_second = models.ForeignKey(ProfileUserModel, on_delete=models.CASCADE, blank=True,
                                    null=True, verbose_name='Второй пользователь', related_name='user_2')

    class Meta:
        verbose_name = "комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return self.name


class MessageChatModel(models.Model):
    """
    Модель сообщения чата
    """

    sender = models.ForeignKey(ProfileUserModel, on_delete=models.CASCADE, verbose_name='Отправитель')
    message = models.TextField(blank=True, null=True, verbose_name='Сообщение')
    room_name = models.ForeignKey(RoomChatModel, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Имя комнаты')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.message


class ChatNotificationModel(models.Model):
    """
    Модель уведомлений в чате
    """
    chat = models.ForeignKey(RoomChatModel, on_delete=models.CASCADE, verbose_name='Чат')
    user = models.ForeignKey(ProfileUserModel, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_seen = models.BooleanField(default=False, verbose_name='Статус')

    class Meta:
        verbose_name = "Уведомления"
        verbose_name_plural = "Уведомление"

    def __str__(self) -> str:
        return self.user.user.username
