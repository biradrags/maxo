"""
Пример мультибот webhook.

Главный бот обрабатывает команды /start и /add.
/add <token> — подписывает вторичного бота на webhook по пути /webhook/bot/{token}.
Вторичные боты отвечают эхом на сообщения.

Переменные окружения:
    TOKEN — токен главного бота
    WEBHOOK_URL — базовый URL webhook (например https://example.com)
    WEBHOOK_SECRET — необязательный секрет для проверки webhook
"""
import logging
import os

from aiohttp import web

from maxo import Bot, Dispatcher
from maxo.omit import Omitted
from maxo.routing.filters import Command, CommandStart
from maxo.routing.updates import MessageCreated
from maxo.routing.utils import collect_used_updates
from maxo.utils.facades import MessageCreatedFacade
from maxo.webhook import (
    AiohttpWebAdapter,
    PathRouting,
    SimpleEngine,
    TokenEngine,
    WebhookConfig,
)
from maxo.webhook.security import Security, StaticSecretToken

main_bot = Bot(os.environ["TOKEN"])
main_dp = Dispatcher()
secondary_dp = Dispatcher()

adapter = AiohttpWebAdapter()
secret = os.environ.get("WEBHOOK_SECRET")
security = Security(StaticSecretToken(secret)) if secret else None


@main_dp.message_created(CommandStart())
async def cmd_start(update: MessageCreated, facade: MessageCreatedFacade) -> None:
    await facade.answer_text("Отправь /add <token>, чтобы зарегистрировать вторичного бота")


@main_dp.message_created(Command("add"))
async def cmd_add(update: MessageCreated, facade: MessageCreatedFacade) -> None:
    text = (update.message.body.text or "").strip()
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await facade.answer_text("Использование: /add <token>")
        return
    token = parts[1].strip()
    webhook_base = os.environ["WEBHOOK_URL"].rstrip("/")
    webhook_url = f"{webhook_base}/webhook/bot/{token}"
    temp_bot = Bot(token=token)
    try:
        await temp_bot.start()
        used = collect_used_updates(secondary_dp)
        update_types = [getattr(u, "value", getattr(u, "name", str(u))) for u in used]
        await temp_bot.subscribe(
            url=webhook_url,
            secret=secret if secret else Omitted(),
            update_types=update_types,
        )
        await facade.answer_text("Вторичный бот подписан на webhook")
    except Exception as e:
        await facade.answer_text(f"Ошибка: {e}")
    finally:
        await temp_bot.close()


@secondary_dp.message_created()
async def secondary_echo(
    update: MessageCreated, facade: MessageCreatedFacade
) -> None:
    text = update.message.body.text or "Нет текста"
    await facade.answer_text(f"[Эхо вторичного бота] {text}")


async def on_startup(app: web.Application) -> None:
    webhook_base = os.environ["WEBHOOK_URL"].rstrip("/")
    main_engine = app["main_engine"]
    await main_engine.set_webhook(
        url=f"{webhook_base}/webhook",
        secret=secret if secret is not None else Omitted(),
    )


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    webhook_base = os.environ.get("WEBHOOK_URL", "http://0.0.0.0:8080").rstrip("/")

    main_routing = StaticRouting(url=f"{webhook_base}/webhook")
    main_engine = SimpleEngine(
        main_dp,
        main_bot,
        web_adapter=adapter,
        routing=main_routing,
        security=security,
        webhook_config=WebhookConfig(),
    )
    main_engine.register(app)
    app["main_engine"] = main_engine

    secondary_routing = PathRouting(url=f"{webhook_base}/webhook/bot/{{bot_token}}")
    secondary_engine = TokenEngine(
        secondary_dp,
        web_adapter=adapter,
        routing=secondary_routing,
        security=security,
        webhook_config=WebhookConfig(),
    )
    secondary_engine.register(app)

    app.on_startup.append(on_startup)
    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
