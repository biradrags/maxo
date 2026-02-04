from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate


class MessageRemoved(MaxUpdate):
    """Вы получите этот `update`, как только сообщение будет удалено."""

    type = UpdateType.MESSAGE_REMOVED

    message_id: str
    chat_id: int
    user_id: int
