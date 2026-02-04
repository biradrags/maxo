from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.chat_member import ChatMember


class ChatMembersList(MaxoType):
    members: list[ChatMember]

    marker: Omittable[int | None] = Omitted()
