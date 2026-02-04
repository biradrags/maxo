from maxo.enums.update_type import UpdateType
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class UserAddedToChat(MaxUpdate):
    """Вы получите это обновление, когда пользователь будет добавлен в чат, где бот является администратором."""

    type = UpdateType.USER_ADDED

    chat_id: int
    user: User
    inviter_id: Omittable[int | None] = Omitted()
    is_channel: bool
