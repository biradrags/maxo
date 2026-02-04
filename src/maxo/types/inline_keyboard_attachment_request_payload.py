from maxo.types.base import MaxoType
from maxo.types.buttons import InlineButtons


class InlineKeyboardAttachmentRequestPayload(MaxoType):
    buttons: list[list[InlineButtons]]
