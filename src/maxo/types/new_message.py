from maxo.enums.text_format import TextFormat
from maxo.types.attachments import Attachments
from maxo.types.base import MaxoType
from maxo.types.new_message_link import NewMessageLink


class NewMessage(MaxoType):
    text: str | None = None
    attachments: list[Attachments] | None = None
    link: NewMessageLink | None = None
    notify: bool = True
    format: TextFormat | None = None
