from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model

from .models import MessageChatModel, RoomChatModel
from accounts.models import ProfileUserModel

User = get_user_model()


def create_chat_name(user_1: int, user_2: int) -> str:
    """
    Создание имени комнаты чата
    :param user_1: id user_1
    :param user_2: id user_2
    :return: str Имя чата комнаты
    """

    if user_1 > user_2:
        room_name = f'chat_{user_1}-{user_2}'
    else:
        room_name = f'chat_{user_2}-{user_1}'

    return room_name


def get_chat_room(room_name: str, user_1, user_2) -> QuerySet:
    """
    Получение или создание комнаты чата
    :param room_name: Имя комнаты
    :param user_1: Пользователь 1
    :param user_2: Пользователь 2
    :return: RoomChatModel objects
    """

    try:
        room = RoomChatModel.objects.get(name=room_name)
    except RoomChatModel.DoesNotExist:
        room = RoomChatModel.objects.create(
            name=room_name,
            user_first=ProfileUserModel.objects.get(user=user_1),
            user_second=ProfileUserModel.objects.get(user=user_2)
        )

    return room


def get_list_rooms_users(user: User) -> QuerySet:
    """
    Получение списка пользователей с которыми есть комната чата
    :param user: User objects
    :return: QuerySet список пользователей
    """

    # Получаем все комнаты, в которых участвует текущий пользователь
    user_rooms = RoomChatModel.objects.filter(
        Q(user_first=ProfileUserModel.objects.get(user=user)) |
        Q(user_second=ProfileUserModel.objects.get(user=user))
    )

    # Получаем список пользователей с которыми есть чат
    users_with_chat = ProfileUserModel.objects.filter(
        Q(user_1__in=user_rooms) | Q(user_2__in=user_rooms)
    ).exclude(user=user)

    # Получаем список имен пользователей
    users_with_chat_names = users_with_chat.values_list('user', flat=True)

    print(users_with_chat)

    return users_with_chat
