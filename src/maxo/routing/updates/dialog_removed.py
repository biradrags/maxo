from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class DialogRemoved(MaxUpdate):
    """Вы получите этот update, когда пользователь удаляет чат."""

    type = UpdateType.DIALOG_REMOVED

    chat_id: int
    user: User
    user_locale: str
