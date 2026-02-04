from maxo.enums.attachment_request_type import AttachmentRequestType
from maxo.omit import Omittable, Omitted
from maxo.types.attachment_request import AttachmentRequest
from maxo.types.buttons import ReplyButtons


class ReplyKeyboardAttachmentRequest(AttachmentRequest):
    """Request to attach reply keyboard to message"""

    type: AttachmentRequestType = AttachmentRequestType.REPLY_KEYBOARD

    buttons: list[list[ReplyButtons]]

    direct: Omittable[bool] = Omitted()
    direct_user_id: Omittable[int | None] = Omitted()
