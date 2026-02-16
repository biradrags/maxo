from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType


class UploadEndpoint(MaxoType):
    """
    Точка доступа, куда следует загружать ваши бинарные файлы

    Args:
        token: Видео- или аудио-токен для отправки сообщения
        url: URL для загрузки файла
    """

    url: str
    """URL для загрузки файла"""

    token: Omittable[str] = Omitted()
    """Видео- или аудио-токен для отправки сообщения"""

    @property
    def unsafe_token(self) -> str:
        if is_defined(self.token):
            return self.token

        raise AttributeIsEmptyError(
            obj=self,
            attr="token",
        )
