from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import ProfileUserModel

User = get_user_model()


class MessageChatModel(models.Model):
    """
    Модель сообщения чата
    """

    sender = models.ForeignKey(ProfileUserModel, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    thread_name = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


# class ChatNotification(models.Model):
#     """
#     Модель уведомлений в чате
#     """
#     chat = models.ForeignKey(MessageChatModel, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_seen = models.BooleanField(default=False)
#
#     def __str__(self) -> str:
#         return self.user.username
#