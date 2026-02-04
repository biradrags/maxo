from maxo.enums.attachment_type import AttachmentType
from maxo.types.base import MaxoType


class Attachment(MaxoType):
    """Общая схема, представляющая вложение сообщения"""

    type: AttachmentType
