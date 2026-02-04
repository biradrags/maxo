from datetime import datetime

from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.omit import Omittable, Omitted
from maxo.types.message_list import MessageList


class GetMessages(MaxoMethod[MessageList]):
    """Получение сообщений."""

    __url__ = "messages"
    __method__ = "get"

    chat_id: Query[Omittable[int]] = Omitted()
    count: Query[Omittable[int]] = Omitted()
    from_: Query[Omittable[datetime]] = Omitted()
    message_ids: Query[Omittable[list[str] | None]] = Omitted()
    to: Query[Omittable[datetime]] = Omitted()
