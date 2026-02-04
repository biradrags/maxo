from enum import StrEnum


class UploadType(StrEnum):
    """
    Тип загружаемого файла

    > Значение `photo` больше не поддерживается. Если вы использовали `type=photo` в ранее созданных интеграциях — замените его на `type=image`
    """

    AUDIO = "audio"
    FILE = "file"
    IMAGE = "image"
    VIDEO = "video"
