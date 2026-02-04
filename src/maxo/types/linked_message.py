from maxo.enums.message_link_type import MessageLinkType
from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.message_body import MessageBody
from maxo.types.user import User


class LinkedMessage(MaxoType):
    message: MessageBody
    type: MessageLinkType

    chat_id: Omittable[int] = Omitted()
    sender: Omittable[User] = Omitted()
