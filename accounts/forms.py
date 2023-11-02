from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import CustomUserModel


class CustomUserCreationForm(UserCreationForm):
    # password1 = forms.CharField(max_length=20, required=True, label='Пароль')
    # password2 = forms.CharField(max_length=20, required=True, label='Подтвердить пароль')

    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', ]
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
