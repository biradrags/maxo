from maxo.enums.text_format import TextFormat
from maxo.omit import Omittable, Omitted
from maxo.types.attachments import AttachmentsRequests
from maxo.types.base import MaxoType
from maxo.types.new_message_link import NewMessageLink


class NewMessageBody(MaxoType):
    attachments: list[AttachmentsRequests] | None = None
    link: NewMessageLink | None = None
    text: str | None = None

    format: Omittable[TextFormat | None] = Omitted()
    notify: Omittable[bool] = Omitted()
