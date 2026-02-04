from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Path
from maxo.omit import Omittable, Omitted
from maxo.types.chat import Chat
from maxo.types.photo_attachment_request_payload import PhotoAttachmentRequestPayload


class EditChat(MaxoMethod[Chat]):
    """Изменение информации о групповом чате."""

    __url__ = "chats/{chat_id}"
    __method__ = "patch"

    chat_id: Path[int]

    icon: Body[Omittable[PhotoAttachmentRequestPayload | None]] = Omitted()
    notify: Body[Omittable[bool | None]] = Omitted()
    pin: Body[Omittable[str | None]] = Omitted()
    title: Body[Omittable[str | None]] = Omitted()
