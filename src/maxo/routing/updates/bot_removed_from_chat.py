from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class BotRemovedFromChat(MaxUpdate):
    """Вы получите этот update, как только бот будет удалён из чата"""

    type = UpdateType.BOT_REMOVED

    chat_id: int
    user: User
    is_channel: bool
