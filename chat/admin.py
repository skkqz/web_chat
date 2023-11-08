from django.contrib import admin
from .models import MessageChatModel


@admin.register(MessageChatModel)
class MessageChatAdmin(admin.ModelAdmin):

    pass
