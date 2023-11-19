from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q

from django.contrib.auth import get_user_model

from .services import create_chat_name
from .models import MessageChatModel, RoomChatModel
from accounts.models import ProfileUserModel

User = get_user_model()


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Представление домашней страницы
    """

    template_name = 'chat/chat_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        return context


class ChatView(LoginRequiredMixin, TemplateView):
    """
    Представление чата
    """

    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])

        room_name = create_chat_name(
            user_1=self.request.user.id,
            user_2=user.id,
        )

        room = RoomChatModel.objects.get_or_create(name=room_name,
                                                   user_first=ProfileUserModel.objects.get(user=self.request.user),
                                                   user_second=ProfileUserModel.objects.get(user=user))

        # Получаем все комнаты, в которых участвует текущий пользователь
        user_rooms = RoomChatModel.objects.filter(
            Q(user_first=ProfileUserModel.objects.get(user=self.request.user)) |
            Q(user_second=ProfileUserModel.objects.get(user=self.request.user))
        )

        # Получаем список пользователей с которыми есть чат
        users_with_chat = ProfileUserModel.objects.filter(
            Q(user_1__in=user_rooms) | Q(user_2__in=user_rooms)
        ).exclude(user=self.request.user)

        # Получаем список имен пользователей
        users_with_chat_names = users_with_chat.values_list('user__username', flat=True)
        print(users_with_chat_names)

        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        context['user'] = user
        context['messages'] = MessageChatModel.objects.filter(room_name=room[0])
        return context
