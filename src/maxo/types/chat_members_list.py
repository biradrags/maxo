from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType
from maxo.types.chat_member import ChatMember


class ChatMembersList(MaxoType):
    """
    Args:
        marker: Указатель на следующую страницу данных
        members: Список участников чата с информацией о времени последней активности
    """

    members: list[ChatMember]
    """Список участников чата с информацией о времени последней активности"""

    marker: Omittable[int | None] = Omitted()
    """Указатель на следующую страницу данных"""

    @property
    def unsafe_marker(self) -> int:
        if is_defined(self.marker):
            return self.marker

        raise AttributeIsEmptyError(
            obj=self,
            attr="marker",
        )
