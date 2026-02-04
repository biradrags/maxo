from unihttp.method import BaseMethod

from maxo.types import MaxoType


class MaxoMethod[_MethodResultT](BaseMethod[_MethodResultT], MaxoType):
    """
    Базовый метод для методов Bot API Max.
    """
