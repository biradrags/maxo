from maxo.omit import Omittable, Omitted
from maxo.types import MaxoType


class LinkPreviewOptions(MaxoType):
    is_disabled: Omittable[bool] = Omitted()
    url: str | None
