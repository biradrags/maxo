from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Path
from maxo.types.simple_query_result import SimpleQueryResult


class AddMembers(MaxoMethod[SimpleQueryResult]):
    """Добавление участников в групповой чат."""

    __url__ = "chats/{chat_id}/members"
    __method__ = "post"

    chat_id: Path[int]

    user_ids: Body[list[int]]
