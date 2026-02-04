from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Path
from maxo.omit import Omittable, Omitted
from maxo.types.simple_query_result import SimpleQueryResult


class PinMessage(MaxoMethod[SimpleQueryResult]):
    """Закрепление сообщения в групповом чате."""

    __url__ = "chats/{chat_id}/pin"
    __method__ = "put"

    chat_id: Path[int]

    message_id: Body[str]
    notify: Body[Omittable[bool | None]] = Omitted()
