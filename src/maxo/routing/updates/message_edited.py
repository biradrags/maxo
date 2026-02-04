from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.message import Message


class MessageEdited(MaxUpdate):
    """Вы получите этот `update`, как только сообщение будет отредактировано."""

    type = UpdateType.MESSAGE_EDITED

    message: Message
