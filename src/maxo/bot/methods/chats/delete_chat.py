from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.simple_query_result import SimpleQueryResult


class DeleteChat(MaxoMethod[SimpleQueryResult]):
    """Удаление группового чата."""

    __url__ = "chats/{chat_id}"
    __method__ = "delete"

    chat_id: Path[int]
