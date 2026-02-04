from datetime import datetime

from maxo.types.base import MaxoType


class Subscription(MaxoType):
    """Схема для описания подписки на WebHook"""

    time: datetime
    url: str

    update_types: list[str] | None = None
