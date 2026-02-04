from maxo.enums import UpdateType
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.base import MaxUpdate
from maxo.types.chat import Chat


# TODO: Что за ивент???
class MessageChatCreated(MaxUpdate):
    """Бот получит это обновление, когда чат будет создан, как только первый пользователь нажмёт кнопку чата."""

    type = UpdateType.MESSAGE_CHAT_CREATED

    chat: Chat
    message_id: str
    start_payload: Omittable[str | None] = Omitted()
