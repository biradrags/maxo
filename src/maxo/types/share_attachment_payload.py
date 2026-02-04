from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ShareAttachmentPayload(MaxoType):
    """Полезная нагрузка запроса ShareAttachmentRequest"""

    token: Omittable[str | None] = Omitted()
    url: Omittable[str | None] = Omitted()
