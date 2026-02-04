from maxo.enums.attachment_type import AttachmentType
from maxo.types.attachment import Attachment


class LocationAttachment(Attachment):
    type: AttachmentType = AttachmentType.LOCATION

    latitude: float
    longitude: float
