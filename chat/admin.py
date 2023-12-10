from django.contrib import admin
from .models import MessageChatModel, RoomChatModel, ChatNotificationModel


@admin.register(MessageChatModel)
class MessageChatAdmin(admin.ModelAdmin):

    pass


@admin.register(RoomChatModel)
class RoomChatAdmin(admin.ModelAdmin):

    pass


@admin.register(ChatNotificationModel)
class ChatNotificationAdmin(admin.ModelAdmin):

    list_display = ['chat', 'user', 'is_seen', ]
