from maxo.types.base import MaxoType
from maxo.types.subscription import Subscription


class GetSubscriptionsResult(MaxoType):
    """Список всех WebHook подписок"""

    subscriptions: list[Subscription]
