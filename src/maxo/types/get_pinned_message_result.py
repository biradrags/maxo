from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType
from maxo.types.message import Message


class GetPinnedMessageResult(MaxoType):
    message: Omittable[Message | None] = Omitted()
