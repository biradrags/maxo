from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class BotAddedToChat(MaxUpdate):
    """Вы получите этот update, как только бот будет добавлен в чат"""

    type = UpdateType.BOT_ADDED

    chat_id: int
    user: User
    is_channel: bool
