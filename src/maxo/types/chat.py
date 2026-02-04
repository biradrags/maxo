from datetime import datetime
from typing import Any

from maxo.enums.chat_status import ChatStatus
from maxo.enums.chat_type import ChatType
from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.image import Image
from maxo.types.message import Message
from maxo.types.user_with_photo import UserWithPhoto


class Chat(MaxoType):
    chat_id: int
    is_public: bool
    last_event_time: datetime
    participants_count: int
    status: ChatStatus
    type: ChatType

    description: str | None = None
    icon: Image | None = None
    title: str | None = None

    chat_message_id: Omittable[str | None] = Omitted()
    dialog_with_user: Omittable[UserWithPhoto | None] = Omitted()
    link: Omittable[str | None] = Omitted()
    owner_id: Omittable[int | None] = Omitted()
    participants: Omittable[dict[str, Any] | None] = Omitted()
    pinned_message: Omittable[Message | None] = Omitted()

    @property
    def id(self) -> int:
        return self.chat_id
