from maxo.types.base import MaxoType
from maxo.types.message import Message


class MessageList(MaxoType):
    """Пагинированный список сообщений"""

    messages: list[Message]
