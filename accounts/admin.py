from django.contrib import admin

from .models import CustomUserModel, ProfileUserModel


@admin.register(CustomUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Кастомная модель администратора
    """

    list_display = [
        "username", 'email'
    ]


@admin.register(ProfileUserModel)
class ProfileUserAdmin(admin.ModelAdmin):
    """
    Модель для профиля пользователя
    """

    model = ProfileUserModel
    list_display = ["user"]
