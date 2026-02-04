from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.omit import Omittable, Omitted
from maxo.types.chat_list import ChatList


class GetChats(MaxoMethod[ChatList]):
    """Получение списка всех групповых чатов."""

    __url__ = "chats"
    __method__ = "get"

    count: Query[Omittable[int]] = Omitted()
    marker: Query[Omittable[int]] = Omitted()
