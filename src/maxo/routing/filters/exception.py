from collections.abc import Callable
from typing import Any, Generic, TypeVar, final

from maxo.routing.ctx import Ctx
from maxo.routing.filters.base import BaseFilter
from maxo.routing.updates import BaseUpdate
from maxo.routing.updates.error import ErrorEvent

_UpdateT = TypeVar("_UpdateT", bound=BaseUpdate)
_ExceptionT = TypeVar("_ExceptionT", bound=Exception)


@final
class ExceptionTypeFilter(
    BaseFilter[ErrorEvent[_ExceptionT, _UpdateT]],
    Generic[_ExceptionT, _UpdateT],
):
    _handler: Callable[[Any], bool]

    __slots__ = ("_handler",)

    def __init__(
        self,
        *errors: type[_ExceptionT],
        use_subclass: bool = True,
    ) -> None:
        if use_subclass:
            self._handler = lambda e: isinstance(e, errors)
        else:
            self._handler = lambda e: type(e) in errors

    async def __call__(
        self,
        update: ErrorEvent[Any, Any],
        ctx: Ctx,
    ) -> bool:
        return self._handler(update.error)
