from django.contrib import admin
from .models import MessageChatModel, RoomChatModel


@admin.register(MessageChatModel)
class MessageChatAdmin(admin.ModelAdmin):

    pass


@admin.register(RoomChatModel)
class RoomChatAdmin(admin.ModelAdmin):

    pass
