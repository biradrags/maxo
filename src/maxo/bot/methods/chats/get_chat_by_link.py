from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.chat import Chat


class GetChatByLink(MaxoMethod[Chat]):
    """Получение группового чата по ссылке."""

    __url__ = "chats/{chat_link}"
    __method__ = "get"

    chat_link: Path[str]
