from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth import get_user_model

from .models import MessageChatModel

User = get_user_model()


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        return context


class ChatView(LoginRequiredMixin, TemplateView):

    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])

        if self.request.user.id > user.id:
            thread_name = f'chat_{self.request.user.id}-{user.id}'
        else:
            thread_name = f'chat_{user.id}-{self.request.user.id}'

        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        context['user'] = user
        context['messages'] = MessageChatModel.objects.filter(thread_name=thread_name)
        return context
