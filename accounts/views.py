from django.urls import reverse_lazy, reverse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView

from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomUserCreationForm

from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(CreateView):
    """
    Регистрация пользователя
    """

    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/signup.html"

