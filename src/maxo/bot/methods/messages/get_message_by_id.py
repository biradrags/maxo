from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.message import Message


class GetMessageById(MaxoMethod[Message]):
    """Получить сообщение."""

    __url__ = "messages/{message_id}"
    __method__ = "get"

    message_id: Path[str]
