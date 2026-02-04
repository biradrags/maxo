from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class UploadedInfo(MaxoType):
    """Это информация, которую вы получите, как только аудио/видео будет загружено"""

    token: Omittable[str] = Omitted()
