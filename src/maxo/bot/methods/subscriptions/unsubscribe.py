from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.types.simple_query_result import SimpleQueryResult


class Unsubscribe(MaxoMethod[SimpleQueryResult]):
    """Отписка от обновлений."""

    __url__ = "subscriptions"
    __method__ = "delete"

    url: Query[str]
