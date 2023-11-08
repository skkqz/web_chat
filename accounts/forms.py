from django.contrib.auth.forms import UserCreationForm

from .models import CustomUserModel


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', ]
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
