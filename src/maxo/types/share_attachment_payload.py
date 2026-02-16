from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType


class ShareAttachmentPayload(MaxoType):
    """
    Полезная нагрузка запроса ShareAttachmentRequest

    Args:
        token: Токен вложения
        url: URL, прикрепленный к сообщению в качестве предпросмотра медиа
    """

    token: Omittable[str | None] = Omitted()
    """Токен вложения"""
    url: Omittable[str | None] = Omitted()
    """URL, прикрепленный к сообщению в качестве предпросмотра медиа"""

    @property
    def unsafe_token(self) -> str:
        if is_defined(self.token):
            return self.token

        raise AttributeIsEmptyError(
            obj=self,
            attr="token",
        )

    @property
    def unsafe_url(self) -> str:
        if is_defined(self.url):
            return self.url

        raise AttributeIsEmptyError(
            obj=self,
            attr="url",
        )
