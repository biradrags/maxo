from maxo.enums.chat_type import ChatType
from maxo.types.base import MaxoType


class Recipient(MaxoType):
    """Новый получатель сообщения. Может быть пользователем или чатом"""

    chat_type: ChatType

    chat_id: int | None = None
    user_id: int | None = None
