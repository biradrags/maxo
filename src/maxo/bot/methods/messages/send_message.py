from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Query
from maxo.enums.text_format import TextFormat
from maxo.omit import Omittable, Omitted
from maxo.types.attachments import AttachmentsRequests
from maxo.types.new_message_link import NewMessageLink
from maxo.types.send_message_result import SendMessageResult


class SendMessage(MaxoMethod[SendMessageResult]):
    """Отправить сообщение."""

    __url__ = "messages"
    __method__ = "post"

    chat_id: Query[Omittable[int]] = Omitted()
    disable_link_preview: Query[Omittable[bool]] = Omitted()
    user_id: Query[Omittable[int]] = Omitted()

    attachments: Body[list[AttachmentsRequests] | None] = None
    link: Body[NewMessageLink | None] = None
    text: Body[str | None] = None
    format: Body[Omittable[TextFormat | None]] = Omitted()
    notify: Body[Omittable[bool]] = Omitted()
