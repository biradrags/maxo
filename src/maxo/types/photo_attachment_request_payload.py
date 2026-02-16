from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType
from maxo.types.photo_token import PhotoToken


class PhotoAttachmentRequestPayload(MaxoType):
    """
    Запрос на прикрепление изображения (все поля являются взаимоисключающими)

    Args:
        photos: Токены, полученные после загрузки изображений
        token: Токен существующего вложения
        url: Любой внешний URL изображения, которое вы хотите прикрепить
    """

    photos: Omittable[list[PhotoToken] | None] = Omitted()  # TODO: Проверить кто это
    """Токены, полученные после загрузки изображений"""
    token: Omittable[str | None] = Omitted()
    """Токен существующего вложения"""
    url: Omittable[str | None] = Omitted()
    """Любой внешний URL изображения, которое вы хотите прикрепить"""

    @property
    def unsafe_photos(self) -> list[PhotoToken]:
        if is_defined(self.photos):
            return self.photos

        raise AttributeIsEmptyError(
            obj=self,
            attr="photos",
        )

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
