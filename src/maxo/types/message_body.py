from maxo.omit import Omittable, Omitted
from maxo.types.attachments import Attachments
from maxo.types.base import MaxoType
from maxo.types.inline_keyboard_attachment import InlineKeyboardAttachment
from maxo.types.keyboard import Keyboard
from maxo.types.markup_elements import MarkupElements


class MessageBody(MaxoType):
    """Схема, представляющая тело сообщения"""

    mid: str
    seq: int

    attachments: list[Attachments] | None = None
    text: str | None = None

    markup: Omittable[list[MarkupElements] | None] = Omitted()

    @property
    def id(self) -> str:
        return self.mid

    @property
    def keyboard(self) -> Keyboard | None:
        if not self.attachments:
            return None
        for attachment in self.attachments:
            if isinstance(attachment, InlineKeyboardAttachment):
                return attachment.payload
        return None

    @property
    def reply_markup(self) -> Keyboard | None:
        return self.keyboard
