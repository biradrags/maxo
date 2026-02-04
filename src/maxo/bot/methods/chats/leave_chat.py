from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.simple_query_result import SimpleQueryResult


class LeaveChat(MaxoMethod[SimpleQueryResult]):
    """Удаление бота из группового чата."""

    __url__ = "chats/{chat_id}/members/me"
    __method__ = "delete"

    chat_id: Path[int]
