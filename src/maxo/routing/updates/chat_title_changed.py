from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class ChatTitleChanged(MaxUpdate):
    """
    BБот получит это обновление, когда будет изменено название чата

    Args:
        chat_id: ID чата, где произошло событие
        title: Новое название
        type:
        user: Пользователь, который изменил название
    """

    type = UpdateType.CHAT_TITLE_CHANGED

    chat_id: int
    """ID чата, где произошло событие"""
    title: str
    """Новое название"""
    user: User
    """Пользователь, который изменил название"""
