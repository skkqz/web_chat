from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth import get_user_model

from .services import create_chat_name, get_list_rooms_users, get_chat_room
from .models import MessageChatModel, RoomChatModel
from accounts.models import ProfileUserModel

User = get_user_model()


class IndexView(LoginRequiredMixin, TemplateView):
    """
    Представление домашней страницы
    """

    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        return context


class ChatView(LoginRequiredMixin, TemplateView):
    """
    Представление чата
    """

    template_name = 'chat/chat_main.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])

        room_name = create_chat_name(
            user_1=self.request.user.id,
            user_2=user.id,
        )

        room = get_chat_room(
            room_name=room_name,
            user_1=self.request.user,
            user_2=user
        )

        users_with_chat_names = get_list_rooms_users(self.request.user)

        context = super().get_context_data(**kwargs)
        context['users'] = users_with_chat_names
        context['user'] = user
        context['messages'] = MessageChatModel.objects.filter(room_name=room)
        return context
