from maxo.types.base import MaxoType
from maxo.types.chat import Chat


class ChatList(MaxoType):
    chats: list[Chat]

    marker: int | None = None
