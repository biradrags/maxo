from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class DialogRemoved(MaxUpdate):
    """
    Вы получите этот update, когда пользователь удаляет чат

    Args:
        chat_id: ID чата, где произошло событие
        type:
        user: Пользователь, который удалил чат
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.DIALOG_REMOVED

    chat_id: int
    """ID чата, где произошло событие"""
    user: User
    """Пользователь, который удалил чат"""
    user_locale: str
    """Текущий язык пользователя в формате IETF BCP 47"""
