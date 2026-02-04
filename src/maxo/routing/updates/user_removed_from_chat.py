from maxo.enums.update_type import UpdateType
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class UserRemovedFromChat(MaxUpdate):
    """Вы получите это обновление, когда пользователь будет удалён из чата, где бот является администратором"""

    type = UpdateType.USER_REMOVED

    chat_id: int
    user: User
    admin_id: Omittable[int] = Omitted()
    is_channel: bool
