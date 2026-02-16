from maxo.enums.message_link_type import MessageLinkType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType
from maxo.types.message_body import MessageBody
from maxo.types.user import User


class LinkedMessage(MaxoType):
    """
    Args:
        chat_id: Чат, в котором сообщение было изначально опубликовано. Только для пересланных сообщений
        message:
        sender: Пользователь, отправивший сообщение.
        type: Тип связанного сообщения
    """

    message: MessageBody
    type: MessageLinkType
    """Тип связанного сообщения"""

    chat_id: Omittable[int] = Omitted()
    """Чат, в котором сообщение было изначально опубликовано. Только для пересланных сообщений"""
    sender: Omittable[User] = Omitted()
    """Пользователь, отправивший сообщение."""

    @property
    def unsafe_chat_id(self) -> int:
        if is_defined(self.chat_id):
            return self.chat_id

        raise AttributeIsEmptyError(
            obj=self,
            attr="chat_id",
        )

    @property
    def unsafe_sender(self) -> User:
        if is_defined(self.sender):
            return self.sender

        raise AttributeIsEmptyError(
            obj=self,
            attr="sender",
        )
