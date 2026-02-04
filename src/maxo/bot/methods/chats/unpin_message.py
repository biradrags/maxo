from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.simple_query_result import SimpleQueryResult


class UnpinMessage(MaxoMethod[SimpleQueryResult]):
    """Удаление закреплённого сообщения в групповом чате."""

    __url__ = "chats/{chat_id}/pin"
    __method__ = "delete"

    chat_id: Path[int]
