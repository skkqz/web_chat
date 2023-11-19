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
