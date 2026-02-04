from maxo.enums.attachment_type import AttachmentType
from maxo.types.attachment import Attachment
from maxo.types.buttons import ReplyButtons


class ReplyKeyboardAttachment(Attachment):
    """Custom reply keyboard in message"""

    type: AttachmentType = AttachmentType.REPLY_KEYBOARD

    buttons: list[list[ReplyButtons]]
