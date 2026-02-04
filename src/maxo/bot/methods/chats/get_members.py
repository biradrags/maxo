from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path, Query
from maxo.omit import Omittable, Omitted
from maxo.types.chat_members_list import ChatMembersList


class GetMembers(MaxoMethod[ChatMembersList]):
    """Получение участников группового чата."""

    __url__ = "chats/{chat_id}/members"
    __method__ = "get"

    chat_id: Path[int]

    count: Query[Omittable[int]] = Omitted()
    marker: Query[Omittable[int]] = Omitted()
    user_ids: Query[Omittable[list[int] | None]] = Omitted()
