from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.get_pinned_message_result import GetPinnedMessageResult


class GetPinnedMessage(MaxoMethod[GetPinnedMessageResult]):
    """Получение закреплённого сообщения в групповом чате."""

    __url__ = "chats/{chat_id}/pin"
    __method__ = "get"

    chat_id: Path[int]
