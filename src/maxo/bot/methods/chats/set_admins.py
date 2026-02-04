from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Path
from maxo.omit import Omittable, Omitted
from maxo.types.chat_admin import ChatAdmin
from maxo.types.simple_query_result import SimpleQueryResult


class SetAdmins(MaxoMethod[SimpleQueryResult]):
    """Назначить администратора группового чата."""

    __url__ = "chats/{chat_id}/members/admins"
    __method__ = "post"

    chat_id: Path[int]

    admins: Body[list[ChatAdmin]]
    marker: Body[Omittable[int | None]] = Omitted()
