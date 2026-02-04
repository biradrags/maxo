from unihttp.http import UploadFile

from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Form, Path
from maxo.types.upload_endpoint import UploadEndpoint


class UploadMedia(MaxoMethod[UploadEndpoint]):
    """
    Загрузка медиа.

    Args:
        upload_url: URL для загрузки медиа.
        file: Загружаемый файл.

    """

    __url__ = "{upload_url}"
    __method__ = "post"

    upload_url: Path[str]
    file: Form[UploadFile]
