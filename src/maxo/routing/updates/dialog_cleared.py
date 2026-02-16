from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class DialogCleared(MaxUpdate):
    """
    Бот получает этот тип обновления сразу после очистки истории диалога.

    Args:
        chat_id: ID чата, где произошло событие
        type:
        user: Пользователь, который включил уведомления
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.DIALOG_CLEARED

    chat_id: int
    """ID чата, где произошло событие"""
    user: User
    """Пользователь, который включил уведомления"""
    user_locale: str
    """Текущий язык пользователя в формате IETF BCP 47"""
