from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class ChatTitleChanged(MaxUpdate):
    """Бот получит это обновление, когда будет изменено название чата"""

    type = UpdateType.CHAT_TITLE_CHANGED

    chat_id: int
    user: User
    title: str
