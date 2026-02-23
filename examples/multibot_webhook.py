"""
Пример мультибот webhook.

Главный бот обрабатывает команды /start и /add.
/add <token> — динамически регистрирует вторичного бота.
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
    BotIdBasedRequestHandler,
    SimpleRequestHandler,
    setup_application,
)

main_bot = Bot(os.environ["TOKEN"])
main_dp = Dispatcher()

secondary_dp = Dispatcher()
# Заполняется в main(); нужен в cmd_add для register_bot
secondary_handler: BotIdBasedRequestHandler | None = None


@main_dp.message_created(CommandStart())
async def cmd_start(update: MessageCreated, facade: MessageCreatedFacade) -> None:
    await facade.answer_text("Отправь /add <token>, чтобы зарегистрировать вторичного бота")


@main_dp.message_created(Command("add"))
async def cmd_add(update: MessageCreated, facade: MessageCreatedFacade) -> None:
    if secondary_handler is None:
        await facade.answer_text("Вторичный handler ещё не готов")
        return
    text = (update.message.body.text or "").strip()
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await facade.answer_text("Использование: /add <token>")
        return
    token = parts[1].strip()
    # Временный бот: получаем bot_id через get_my_info и подписываем на webhook
    temp_bot = Bot(token=token)
    try:
        await temp_bot.start()
        bot_id = temp_bot.state.info.user_id
        webhook_url = os.environ["WEBHOOK_URL"]
        secret = os.environ.get("WEBHOOK_SECRET")
        url = f"{webhook_url.rstrip('/')}/webhook/b/{bot_id}"
        update_types = list(collect_used_updates(secondary_dp))
        await temp_bot.subscribe(
            url=url,
            secret=secret if secret else Omitted(),
            update_types=update_types,
        )
        # Регистрируем бота в handler — он будет обрабатывать входящие обновления по bot_id
        await secondary_handler.register_bot(bot_id, token)
        await facade.answer_text(f"Вторичный бот зарегистрирован (id={bot_id})")
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
    """Подписываем главного бота на webhook при старте приложения."""
    webhook_url = os.environ["WEBHOOK_URL"]
    secret = os.environ.get("WEBHOOK_SECRET")
    handler = app["main_handler"]
    await handler.setup_webhook(
        url=f"{webhook_url.rstrip('/')}/webhook",
        secret=secret if secret is not None else Omitted(),
    )


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    secret = os.environ.get("WEBHOOK_SECRET")

    # Главный бот: один маршрут /webhook
    main_handler = SimpleRequestHandler(
        dispatcher=main_dp, bot=main_bot, secret_token=secret
    )
    main_handler.register(app, path="/webhook")
    app["main_handler"] = main_handler
    setup_application(app, main_dp, bot=main_bot)

    # Вторичные боты: маршрут /webhook/b/{bot_id}, боты добавляются через register_bot
    global secondary_handler
    secondary_handler = BotIdBasedRequestHandler(
        dispatcher=secondary_dp, secret_token=secret
    )
    secondary_handler.register(app, path="/webhook/b/{bot_id}")
    setup_application(app, secondary_dp)

    app.on_startup.append(on_startup)
    web.run_app(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
