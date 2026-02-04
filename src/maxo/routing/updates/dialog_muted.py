from datetime import datetime

from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class DialogMuted(MaxUpdate):
    """Вы получите этот update, когда пользователь заглушит диалог с ботом"""

    type = UpdateType.DIALOG_MUTED
    chat_id: int
    user: User
    muted_until: datetime
    user_locale: str
