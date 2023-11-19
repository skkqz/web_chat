from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.managers import CustomUserManager

from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserModel(AbstractUser):
    """
    Кастомная модель пользователя
    """

    username = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name='Имя пользователя')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class ProfileUserModel(models.Model):
    """
    Модель профиля пользователя
    """

    user = models.OneToOneField(
        "CustomUserModel",
        on_delete=models.CASCADE,
        verbose_name="Профиль",
        related_name="profile",
        blank=True,
        null=True,
    )
    online_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=CustomUserModel)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Сигналы для создания профиля пользователя
    """

    if created:
        ProfileUserModel.objects.create(user=instance)


@receiver(post_save, sender=CustomUserModel)
def save_user_profile(sender, instance, **kwargs):
    """
    Сигналы для сохранения профиля пользователя
    """

    instance.profile.save()
