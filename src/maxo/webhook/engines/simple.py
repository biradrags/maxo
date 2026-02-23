from __future__ import annotations

from typing import TYPE_CHECKING, Any

from maxo.bot.methods.subscriptions.subscribe import Subscribe
from maxo.omit import Omittable, Omitted, is_defined

from maxo.webhook.adapters.base import BoundRequest, WebAdapter
from maxo.webhook.config.webhook import WebhookConfig
from maxo.webhook.engines.base import WebhookEngine
from maxo.webhook.routing.base import BaseRouting

if TYPE_CHECKING:
    from collections.abc import Sequence

    from maxo.bot.bot import Bot
    from maxo.routing.dispatcher import Dispatcher

    from maxo.webhook.security.checks import Security


class SimpleEngine(WebhookEngine):
    def __init__(
        self,
        dispatcher: Dispatcher,
        bot: Bot,
        *,
        web_adapter: WebAdapter,
        routing: BaseRouting,
        security: Security | None = None,
        webhook_config: WebhookConfig | None = None,
        handle_in_background: bool = True,
    ) -> None:
        super().__init__(
            dispatcher,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
            handle_in_background=handle_in_background,
        )
        self.bot = bot
        self.webhook_config = webhook_config or WebhookConfig()

    async def _resolve_bot(self, bound_request: BoundRequest) -> Bot | None:
        return self.bot

    async def set_webhook(
        self,
        url: str | None = None,
        secret: Omittable[str] = Omitted(),
        update_types: Omittable[Sequence[str]] = Omitted(),
    ) -> Bot:
        if not self.bot.state.started:
            await self.bot.start()

        effective_url = url or self.routing.webhook_point(self.bot)
        if is_defined(update_types):
            types_list = list(update_types)
        else:
            types_list = self.webhook_config.resolve_allowed_updates(self.dispatcher)

        effective_secret: Omittable[str] = Omitted()
        if is_defined(secret):
            effective_secret = secret
        elif self.security is not None:
            got = await self.security.get_secret_token(self.bot)
            if got is not None:
                effective_secret = got

        await self.bot.call_method(
            Subscribe(url=effective_url, secret=effective_secret, update_types=types_list),
        )
        return self.bot

    async def on_startup(self, app: Any, *args: Any, **kwargs: Any) -> None:
        from maxo.routing.signals.startup import AfterStartup, BeforeStartup

        workflow_data = {
            "app": app,
            "dispatcher": self.dispatcher,
            "bot": self.bot,
            **self.dispatcher.workflow_data,
            **kwargs,
        }
        self.dispatcher.workflow_data.update(workflow_data)
        await self.dispatcher.feed_signal(BeforeStartup(), self.bot)
        await self.dispatcher.feed_signal(AfterStartup(), self.bot)

    async def on_shutdown(self, app: Any, *args: Any, **kwargs: Any) -> None:
        from maxo.routing.signals.shutdown import AfterShutdown, BeforeShutdown

        await self._background.wait_all()
        workflow_data = {
            "app": app,
            "dispatcher": self.dispatcher,
            "bot": self.bot,
            **kwargs,
        }
        await self.dispatcher.feed_signal(BeforeShutdown(), self.bot)
        await self.dispatcher.feed_signal(AfterShutdown(), self.bot)
        await self.bot.close()
