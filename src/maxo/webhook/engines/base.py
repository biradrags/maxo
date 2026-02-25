from __future__ import annotations

from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import TYPE_CHECKING, Any

from adaptix.load_error import AggregateLoadError, LoadError
from aiohttp.client_exceptions import ContentTypeError

from maxo import loggers
from maxo.routing.signals.update import MaxoUpdate
from maxo.webhook.adapters.base import BoundRequest, WebAdapter
from maxo.webhook.background.manager import BackgroundTaskManager
from maxo.webhook.parsing.parser import AdaptixUpdateParser
from maxo.webhook.routing.base import BaseRouting

if TYPE_CHECKING:
    from maxo.bot.bot import Bot
    from maxo.routing.dispatcher import Dispatcher
    from maxo.webhook.security.checks import Security


def _content_type_ok(headers: dict[str, str]) -> bool:
    ct = next((v for k, v in headers.items() if k.lower() == "content-type"), None)
    if not ct:
        return False
    media_type = ct.split(";", 1)[0].strip().lower()
    return media_type == "application/json" or media_type.endswith("+json")


class WebhookEngine(ABC):
    def __init__(
        self,
        dispatcher: Dispatcher,
        *,
        web_adapter: WebAdapter,
        routing: BaseRouting,
        security: Security | None = None,
        handle_in_background: bool = True,
    ) -> None:
        self.dispatcher = dispatcher
        self.web_adapter = web_adapter
        self.routing = routing
        self.security = security
        self.handle_in_background = handle_in_background
        self._parser = AdaptixUpdateParser()
        self._background = BackgroundTaskManager()

    @abstractmethod
    async def _resolve_bot(self, bound_request: BoundRequest) -> Bot | None:
        raise NotImplementedError

    @abstractmethod
    async def set_webhook(self, *args: Any, **kwargs: Any) -> Bot:
        raise NotImplementedError

    @abstractmethod
    async def on_startup(self, app: Any, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    async def on_shutdown(self, app: Any, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def register(self, app: Any) -> None:
        self.web_adapter.register(
            app=app,
            path=self.routing.path,
            handler=self.handle_request,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )

    async def handle_request(self, bound_request: BoundRequest) -> Any:
        bot = await self._resolve_bot(bound_request)
        if bot is None:
            return self.web_adapter.create_json_response(
                status=400,
                payload={"detail": "Bot not found"},
            )

        if self.security is not None and not await self.security.verify(
            bot=bot,
            bound_request=bound_request,
        ):
            loggers.webhook.warning("Unauthorized webhook request")
            if hasattr(self.web_adapter, "create_text_response"):
                return self.web_adapter.create_text_response(
                    status=401,
                    text="Unauthorized",
                )
            return self.web_adapter.create_json_response(
                status=401,
                payload={"detail": "Unauthorized"},
            )

        if not _content_type_ok(bound_request.headers):
            ct = bound_request.headers.get("Content-Type") or bound_request.headers.get(
                "content-type",
            )
            loggers.webhook.warning("Invalid content type: %s", ct)
            return self.web_adapter.create_text_response(
                status=400,
                text="Invalid Content-Type, expected JSON",
            )

        try:
            raw = await bound_request.json()
        except (ContentTypeError, JSONDecodeError):
            loggers.webhook.warning("Invalid webhook request body")
            return self.web_adapter.create_text_response(
                status=400,
                text="Invalid JSON body",
            )

        if not isinstance(raw, dict):
            loggers.webhook.warning(
                "Invalid webhook payload type: %s",
                type(raw).__name__,
            )
            return self.web_adapter.create_text_response(
                status=400,
                text="Webhook payload must be a JSON object",
            )

        try:
            parsed = self._parser.parse(raw)
        except (LoadError, AggregateLoadError):
            return self.web_adapter.create_text_response(
                status=400,
                text="Invalid webhook update payload",
            )

        maxo_update = MaxoUpdate(update=parsed)

        if self.handle_in_background:
            self._background.spawn(
                self._feed_update(bot, maxo_update),
            )
            return self.web_adapter.create_json_response(status=200, payload={})

        await self._feed_update(bot, maxo_update)
        return self.web_adapter.create_json_response(status=200, payload={})

    async def _feed_update(self, bot: Bot, update: MaxoUpdate[Any]) -> None:
        await self.dispatcher.feed_max_update(update, bot)
