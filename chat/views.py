from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth import get_user_model

User = get_user_model()


class IndexView(TemplateView):

    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        return context


class ChatView(TemplateView):

    template_name = 'chat/index.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])

        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username=self.request.user.username)
        context['user'] = user
        return context
