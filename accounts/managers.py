from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        """
        Кастомное создание пользователя
        """

        if not email:
            raise ValueError("Введите электронную почту")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Кастомное создание супер пользователя
        """

        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь статус персонала")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")
        return self.create_user(email, password, **kwargs)
