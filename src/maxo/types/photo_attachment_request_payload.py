from maxo.omit import Omittable, Omitted
from maxo.types.photo_token import PhotoToken
from maxo.types.base import MaxoType


class PhotoAttachmentRequestPayload(MaxoType):
    """Запрос на прикрепление изображения (все поля являются взаимоисключающими)"""

    photos: Omittable[list[PhotoToken] | None] = Omitted()  # TODO: Проверить кто это
    token: Omittable[str | None] = Omitted()
    url: Omittable[str | None] = Omitted()
