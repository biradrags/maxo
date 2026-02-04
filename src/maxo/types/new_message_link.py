from maxo.enums.message_link_type import MessageLinkType
from maxo.types.base import MaxoType


class NewMessageLink(MaxoType):
    mid: str
    type: MessageLinkType
