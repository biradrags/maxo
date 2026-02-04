from maxo.types.base import MaxoType


class PhotoAttachmentPayload(MaxoType):
    photo_id: int
    token: str
    url: str
