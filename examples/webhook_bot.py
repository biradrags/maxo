import logging
import os

from aiohttp import web
from maxo import Bot, Dispatcher
from maxo.routing.updates import MessageCreated
from maxo.utils.facades import MessageCreatedFacade
from maxo.webhook.aiohttp_server import SimpleRequestHandler, setup_application

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
    handler = app["webhook_handler"]
    await handler.setup_webhook(url=webhook_url, secret=secret)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    app = web.Application()
    handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=os.environ.get("WEBHOOK_SECRET"),
    )
    handler.register(app, path="/webhook")
    app["webhook_handler"] = handler
    setup_application(app, dp)

    app.on_startup.append(on_startup)
    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
