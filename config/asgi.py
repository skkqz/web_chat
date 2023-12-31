import os

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from chat.consumers import PersonalChatConsumer, OnlineStatusConsumer, ChatNotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
            path('ws/online/', OnlineStatusConsumer.as_asgi()),
            path('ws/notifications/', ChatNotificationConsumer.as_asgi()),
        ])
    )
})