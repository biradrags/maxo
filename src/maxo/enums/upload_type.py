from enum import StrEnum


class UploadType(StrEnum):
    """
    Тип загружаемого файла

    Поддерживаемые форматы:
    - `image`: JPG, JPEG, PNG, GIF, TIFF, BMP, HEIC
    - `video`: MP4, MOV, MKV, WEBM, MATROSKA
    - `audio`: MP3, WAV, M4A и другие
    - `file`: любые типы файлов

    > Значение `photo` больше не поддерживается. Если вы использовали `type=photo` в ранее созданных интеграциях — замените его на `type=image`
    """

    AUDIO = "audio"
    FILE = "file"
    IMAGE = "image"
    VIDEO = "video"
