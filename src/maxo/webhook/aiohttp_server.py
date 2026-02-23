from __future__ import annotations

import asyncio
import secrets
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from aiohttp import web

from maxo import loggers
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.utils import collect_used_updates

if TYPE_CHECKING:
    from adaptix import Retort

from maxo.bot.bot import Bot
from maxo.routing.dispatcher import Dispatcher
from maxo.routing.signals.shutdown import AfterShutdown, BeforeShutdown
from maxo.routing.signals.startup import AfterStartup, BeforeStartup
from maxo.routing.signals.update import MaxoUpdate
from maxo.routing.updates import Updates
from maxo.serialization import create_response_loader


def setup_application(
    app: web.Application,
    dispatcher: Dispatcher,
    /,
    **kwargs: Any,
) -> None:
    workflow_data = {
        "app": app,
        "dispatcher": dispatcher,
        **dispatcher.workflow_data,
        **kwargs,
    }
    dispatcher.workflow_data.update(workflow_data)

    async def on_startup(*a: Any, **kw: Any) -> None:
        await dispatcher.feed_signal(BeforeStartup())
        await dispatcher.feed_signal(AfterStartup())

    async def on_shutdown(*a: Any, **kw: Any) -> None:
        await dispatcher.feed_signal(BeforeShutdown())
        await dispatcher.feed_signal(AfterShutdown())

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


class BaseRequestHandler(ABC):
    def __init__(
        self,
        dispatcher: Dispatcher,
        handle_in_background: bool = True,
        **data: Any,
    ) -> None:
        self.dispatcher = dispatcher
        self.handle_in_background = handle_in_background
        self._background_feed_update_tasks: set[asyncio.Task[Any]] = set()
        self._retort: Retort = create_response_loader()

    def register(
        self,
        app: web.Application,
        /,
        path: str,
        **kwargs: Any,
    ) -> None:
        app.on_shutdown.append(self._handle_close)
        app.router.add_route("POST", path, self.handle, **kwargs)

    async def _handle_close(self, *a: Any, **kw: Any) -> None:
        await self.close()

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def resolve_bot(self, request: web.Request) -> Bot:
        ...

    @abstractmethod
    def verify_secret(self, secret_header: str, bot: Bot) -> bool:
        ...

    def _parse_update(self, data: dict[str, Any]) -> Updates:  # type: ignore[valid-type]
        return self._retort.load(data, Updates)

    async def _background_feed_update(
        self,
        bot: Bot,
        update: MaxoUpdate[Any],
    ) -> None:
        await self.dispatcher.feed_max_update(update, bot)

    async def _handle_request_background(
        self,
        bot: Bot,
        request: web.Request,
    ) -> web.Response:
        update_data = await request.json()
        parsed = self._parse_update(update_data)
        maxo_update = MaxoUpdate(update=parsed)
        task = asyncio.create_task(
            self._background_feed_update(bot, maxo_update),
        )
        self._background_feed_update_tasks.add(task)
        task.add_done_callback(self._background_feed_update_tasks.discard)
        return web.json_response({})

    async def _handle_request(
        self,
        bot: Bot,
        request: web.Request,
    ) -> web.Response:
        update_data = await request.json()
        parsed = self._parse_update(update_data)
        maxo_update = MaxoUpdate(update=parsed)
        await self.dispatcher.feed_max_update(maxo_update, bot)
        return web.json_response({})

    async def handle(self, request: web.Request) -> web.Response:
        bot = await self.resolve_bot(request)
        secret_header = request.headers.get("X-Max-Bot-Api-Secret", "")
        if not self.verify_secret(secret_header, bot):
            loggers.webhook.warning("Unauthorized webhook request")
            return web.Response(body="Unauthorized", status=401)
        if self.handle_in_background:
            return await self._handle_request_background(bot, request)
        return await self._handle_request(bot, request)

    __call__ = handle


class SimpleRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        secret_token: str | None = None,
        handle_in_background: bool = True,
        **data: Any,
    ) -> None:
        super().__init__(
            dispatcher=dispatcher,
            handle_in_background=handle_in_background,
            **data,
        )
        self.bot = bot
        self.secret_token = secret_token

    def verify_secret(self, secret_header: str, bot: Bot) -> bool:
        if self.secret_token:
            return secrets.compare_digest(secret_header, self.secret_token)
        return True

    async def close(self) -> None:
        await self.bot.close()

    async def resolve_bot(self, request: web.Request) -> Bot:
        return self.bot

    async def setup_webhook(
        self,
        url: str,
        secret: Omittable[str] = Omitted(),
        update_types: Omittable[Sequence[str]] = Omitted(),
    ) -> None:
        if not self.bot.state.started:
            await self.bot.start()
        types = list(update_types or collect_used_updates(self.dispatcher))
        effective_secret: Omittable[str] = Omitted()
        if is_defined(secret):
            effective_secret = secret
        elif self.secret_token:
            effective_secret = self.secret_token
        await self.bot.subscribe(
            url=url, secret=effective_secret, update_types=types
        )


class TokenBasedRequestHandler(BaseRequestHandler):
    def __init__(
        self,
        dispatcher: Dispatcher,
        handle_in_background: bool = True,
        bot_settings: dict[str, Any] | None = None,
        **data: Any,
    ) -> None:
        super().__init__(
            dispatcher=dispatcher,
            handle_in_background=handle_in_background,
            **data,
        )
        self.bot_settings: dict[str, Any] = bot_settings or {}
        self.bots: dict[str, Bot] = {}

    def verify_secret(self, secret_header: str, bot: Bot) -> bool:
        return True

    async def close(self) -> None:
        for bot in self.bots.values():
            await bot.close()

    def register(
        self,
        app: web.Application,
        /,
        path: str,
        **kwargs: Any,
    ) -> None:
        if "{bot_token}" not in path:
            msg = "Path should contain '{bot_token}' substring"
            raise ValueError(msg)
        super().register(app, path=path, **kwargs)

    async def resolve_bot(self, request: web.Request) -> Bot:
        token = request.match_info["bot_token"]
        if token not in self.bots:
            bot = Bot(token=token, **self.bot_settings)
            await bot.start()
            self.bots[token] = bot
        return self.bots[token]
