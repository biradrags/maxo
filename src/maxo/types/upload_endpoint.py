from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class UploadEndpoint(MaxoType):
    """Точка доступа, куда следует загружать ваши бинарные файлы"""

    url: str

    token: Omittable[str] = Omitted()
