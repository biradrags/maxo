from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class DialogUnmuted(MaxUpdate):
    """Вы получите этот update, когда пользователь включит уведомления в диалоге с ботом."""

    type = UpdateType.DIALOG_UNMUTED

    chat_id: int
    user: User
    user_locale: str
