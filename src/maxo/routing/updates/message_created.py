from maxo.enums.update_type import UpdateType
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.base import MaxUpdate
from maxo.types.message import Message


class MessageCreated(MaxUpdate):
    """Вы получите этот `update`, как только сообщение будет создано."""

    type = UpdateType.MESSAGE_CREATED

    message: Message
    user_locale: Omittable[str | None] = Omitted()
