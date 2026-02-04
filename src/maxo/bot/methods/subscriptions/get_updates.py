from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.omit import Omittable, Omitted
from maxo.types.update_list import UpdateList


class GetUpdates(MaxoMethod[UpdateList]):
    """Получение обновлений."""

    __url__ = "updates"
    __method__ = "get"

    limit: Query[Omittable[int]] = Omitted()
    marker: Query[Omittable[int | None]] = Omitted()
    timeout: Query[Omittable[int]] = Omitted()
    types: Query[Omittable[list[str] | None]] = Omitted()
