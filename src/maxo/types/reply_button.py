from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ReplyButton(MaxoType):
    """After pressing this type of button client will send a message on behalf of user with given payload"""

    text: str

    payload: Omittable[str | None] = Omitted()
