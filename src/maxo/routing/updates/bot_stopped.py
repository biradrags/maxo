from maxo.enums.update_type import UpdateType
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class BotStopped(MaxUpdate):
    """Бот получает этот тип обновления, как только пользователь останавливает бота"""

    type = UpdateType.BOT_STOPPED

    chat_id: int
    user: User
    user_locale: Omittable[str] = Omitted()
