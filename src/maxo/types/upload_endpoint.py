from maxo.types.base import MaxoType


class UploadEndpoint(MaxoType):
    """Точка доступа, куда следует загружать ваши бинарные файлы"""

    token: str
    url: str
