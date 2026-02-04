from maxo.enums.attachment_request_type import AttachmentRequestType
from maxo.types.attachment_request import AttachmentRequest


class LocationAttachmentRequest(AttachmentRequest):
    """Запрос на прикрепление клавиатуры к сообщению"""

    type: AttachmentRequestType = AttachmentRequestType.LOCATION

    latitude: float
    longitude: float
