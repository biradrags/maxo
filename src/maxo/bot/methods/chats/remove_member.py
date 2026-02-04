from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path, Query
from maxo.omit import Omittable, Omitted
from maxo.types.simple_query_result import SimpleQueryResult


class RemoveMember(MaxoMethod[SimpleQueryResult]):
    """Удаление участника из группового чата."""

    __url__ = "chats/{chat_id}/members"
    __method__ = "delete"

    chat_id: Path[int]

    user_id: Query[int]
    block: Query[Omittable[bool]] = Omitted()
