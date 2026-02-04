from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class SimpleQueryResult(MaxoType):
    """Простой ответ на запрос"""

    success: bool

    message: Omittable[str] = Omitted()
