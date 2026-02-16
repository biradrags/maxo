from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class BotRemovedFromChat(MaxUpdate):
    """
    Вы получите этот update, как только бот будет удалён из чата

    Args:
        chat_id: ID чата, откуда был удалён бот
        is_channel: Указывает, был ли бот удалён из канала или нет
        type:
        user: Пользователь, удаливший бота из чата
    """

    type = UpdateType.BOT_REMOVED

    chat_id: int
    """ID чата, откуда был удалён бот"""
    is_channel: bool
    """Указывает, был ли бот удалён из канала или нет"""
    user: User
    """Пользователь, удаливший бота из чата"""
