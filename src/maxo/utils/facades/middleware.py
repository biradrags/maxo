from collections.abc import Mapping
from typing import Any, final

from maxo.routing.ctx import Ctx
from maxo.routing.interfaces.middleware import BaseMiddleware, NextMiddleware
from maxo.routing.signals.update import MaxoUpdate
from maxo.routing.updates.base import BaseUpdate
from maxo.routing.updates.message_callback import MessageCallback
from maxo.routing.updates.message_created import MessageCreated
from maxo.utils.facades.updates.base import BaseUpdateFacade
from maxo.utils.facades.updates.message_callback import MessageCallbackFacade
from maxo.utils.facades.updates.message_created import MessageCreatedFacade

_FACADES_MAP: Mapping[type[Any], type[BaseUpdateFacade[Any]]] = {
    MessageCreated: MessageCreatedFacade,
    MessageCallback: MessageCallbackFacade,
}


class FacadeMiddleware(BaseMiddleware[MaxoUpdate[Any]]):
    @final
    async def __call__(
        self,
        update: MaxoUpdate[Any],
        ctx: Ctx,
        next: NextMiddleware[MaxoUpdate[Any]],
    ) -> Any:
        facade = self._facade_cls_factory(type(update.update))
        if facade:
            ctx["facade"] = facade(ctx["bot"], update.update)

        return await next(ctx)

    def _facade_cls_factory(
        self,
        update_tp: type[BaseUpdate],
    ) -> type[BaseUpdateFacade[Any]] | None:
        return _FACADES_MAP.get(update_tp)
