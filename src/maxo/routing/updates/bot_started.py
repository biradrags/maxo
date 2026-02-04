from maxo.enums.update_type import UpdateType
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class BotStarted(MaxUpdate):
    """Бот получает этот тип обновления, как только пользователь нажал кнопку `Start`"""

    type = UpdateType.BOT_STARTED

    chat_id: int
    user: User
    payload: Omittable[str | None] = Omitted()
    user_locale: Omittable[str] = Omitted()
