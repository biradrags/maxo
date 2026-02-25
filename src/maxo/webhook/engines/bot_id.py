from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

from maxo.bot.methods.subscriptions.subscribe import Subscribe
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.signals.shutdown import AfterShutdown, BeforeShutdown
from maxo.routing.signals.startup import AfterStartup, BeforeStartup
from maxo.webhook.adapters.base import BoundRequest, WebAdapter
from maxo.webhook.config.webhook import WebhookConfig
from maxo.webhook.engines.base import WebhookEngine
from maxo.webhook.routing.base import BotIdRouting

if TYPE_CHECKING:
    from collections.abc import Sequence

    from maxo.bot.bot import Bot
    from maxo.routing.dispatcher import Dispatcher
    from maxo.webhook.security.checks import Security


class BotIdEngine(WebhookEngine):
    def __init__(
        self,
        dispatcher: Dispatcher,
        *,
        web_adapter: WebAdapter,
        routing: BotIdRouting,
        security: Security | None = None,
        webhook_config: WebhookConfig | None = None,
        bot_settings: dict[str, Any] | None = None,
        handle_in_background: bool = True,
    ) -> None:
        super().__init__(
            dispatcher,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
            handle_in_background=handle_in_background,
        )
        self.routing: BotIdRouting = routing
        self.webhook_config = webhook_config or WebhookConfig()
        self.bot_settings = bot_settings or {}
        self._registry: dict[int, str] = {}
        self._bots: dict[str, Bot] = {}
        self._started_tokens: set[str] = set()
        self._lock = asyncio.Lock()
        self._app: Any = None

    def register(self, app: Any) -> None:
        self._app = app
        super().register(app)

    async def register_bot(self, bot_id: int, token: str) -> None:
        self._registry[bot_id] = token

    async def unregister_bot(self, bot_id: int) -> None:
        self._registry.pop(bot_id, None)

    async def _startup_bot(self, bot: Bot, token: str) -> None:
        if token in self._started_tokens:
            return
        workflow_data = {
            "app": self._app,
            "dispatcher": self.dispatcher,
            "bot": bot,
            **self.dispatcher.workflow_data,
        }
        self.dispatcher.workflow_data.update(workflow_data)
        await self.dispatcher.feed_signal(BeforeStartup(), bot)
        await self.dispatcher.feed_signal(AfterStartup(), bot)
        self._started_tokens.add(token)

    async def _resolve_bot(self, bound_request: BoundRequest) -> Bot | None:
        bot_id = self.routing.extract_bot_id(bound_request)
        if bot_id is None:
            return None
        token = self._registry.get(bot_id)
        if not token:
            return None
        async with self._lock:
            if token in self._bots:
                return self._bots[token]
            from maxo.bot.bot import Bot  # noqa: PLC0415

            bot = Bot(token=token, **self.bot_settings)
            await bot.start()
            self._bots[token] = bot
        await self._startup_bot(self._bots[token], token)
        return self._bots[token]

    async def _get_or_create_bot(self, bot_id: int) -> Bot | None:
        token = self._registry.get(bot_id)
        if not token:
            return None
        async with self._lock:
            if token in self._bots:
                return self._bots[token]
            from maxo.bot.bot import Bot  # noqa: PLC0415

            bot = Bot(token=token, **self.bot_settings)
            await bot.start()
            self._bots[token] = bot
        await self._startup_bot(self._bots[token], token)
        return self._bots[token]

    async def set_webhook(
        self,
        bot_id: int,
        url: str | None = None,
        secret: Omittable[str] = Omitted(),
        update_types: Omittable[Sequence[str]] = Omitted(),
    ) -> Bot:
        bot = await self._get_or_create_bot(bot_id)
        if bot is None:
            raise ValueError(f"Bot id {bot_id} not registered")
        effective_url = url or self.routing.webhook_point_for_id(bot_id)
        if is_defined(update_types):
            types_list = list(update_types)
        else:
            types_list = self.webhook_config.resolve_allowed_updates(self.dispatcher)
        effective_secret: Omittable[str] = Omitted()
        if is_defined(secret):
            effective_secret = secret
        elif self.security is not None:
            got = await self.security.get_secret_token(bot)
            if got is not None:
                effective_secret = got
        await bot.call_method(
            Subscribe(
                url=effective_url,
                secret=effective_secret,
                update_types=types_list,
            ),
        )
        return bot

    async def on_startup(self, app: Any, *args: Any, **kwargs: Any) -> None:
        self._app = app
        self.dispatcher.workflow_data.update(
            {"app": app, "dispatcher": self.dispatcher, **kwargs},
        )
        for token, bot in list(self._bots.items()):
            await self._startup_bot(bot, token)

    async def on_shutdown(self, app: Any, *args: Any, **kwargs: Any) -> None:
        await self._background.wait_all()
        self.dispatcher.workflow_data.update(
            {"app": app, "dispatcher": self.dispatcher, **kwargs},
        )
        for bot in list(self._bots.values()):
            await self.dispatcher.feed_signal(BeforeShutdown(), bot)
            await self.dispatcher.feed_signal(AfterShutdown(), bot)
        for bot in self._bots.values():
            await bot.close()
        self._bots.clear()
        self._started_tokens.clear()
