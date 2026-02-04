from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body
from maxo.omit import Omittable, Omitted
from maxo.types.simple_query_result import SimpleQueryResult


class Subscribe(MaxoMethod[SimpleQueryResult]):
    """Подписка на обновления."""

    __url__ = "subscriptions"
    __method__ = "post"

    url: Body[str]
    secret: Body[Omittable[str]] = Omitted()
    update_types: Body[Omittable[list[str]]] = Omitted()
