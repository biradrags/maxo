import logging
import os

from aiohttp import web

from maxo import Bot, Dispatcher
from maxo.omit import Omitted
from maxo.routing.updates import MessageCreated
from maxo.utils.facades import MessageCreatedFacade
from maxo.webhook import (
    AiohttpWebAdapter,
    SimpleEngine,
    StaticRouting,
    WebhookConfig,
)
from maxo.webhook.security import Security, StaticSecretToken

bot = Bot(os.environ["TOKEN"])
dp = Dispatcher()


@dp.message_created()
async def echo_handler(
    update: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    text = update.message.body.text or "Текста нет"
    await facade.answer_text(text)


async def on_startup(app: web.Application) -> None:
    webhook_url = os.environ["WEBHOOK_URL"]
    secret = os.environ.get("WEBHOOK_SECRET")
    await bot.start()
    engine = app["webhook_engine"]
    await engine.set_webhook(
        url=webhook_url,
        secret=secret if secret is not None else Omitted(),
    )


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    host = os.environ.get("WEBHOOK_HOST", "127.0.0.1")
    port = int(os.environ.get("WEBHOOK_PORT", "8080"))

    app = web.Application()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url=os.environ.get("WEBHOOK_URL", f"http://{host}:{port}/webhook"))
    secret = os.environ.get("WEBHOOK_SECRET")
    security = Security(StaticSecretToken(secret)) if secret else None
    engine = SimpleEngine(
        dp,
        bot,
        web_adapter=adapter,
        routing=routing,
        security=security,
        webhook_config=WebhookConfig(),
    )
    engine.register(app)
    app["webhook_engine"] = engine
    app.on_startup.append(on_startup)
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()
