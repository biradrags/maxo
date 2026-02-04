from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.chat_admin import ChatAdmin


class ChatAdminsList(MaxoType):
    admins: list[ChatAdmin]

    marker: Omittable[int | None] = Omitted()
