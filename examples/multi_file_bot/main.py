"""
Бот, разнесённый по файлам: точка входа main.py и роутеры в handlers/.
Запуск из корня репозитория: python examples/multi_file_bot/main.py
или из этой папки: python main.py
"""
import logging
import os
import sys
from pathlib import Path

# Чтобы из этой папки импортировать handlers при любом текущем каталоге
sys.path.insert(0, str(Path(__file__).resolve().parent))

from maxo import Bot, Dispatcher
from maxo.utils.long_polling import LongPolling

from handlers import echo_router, start_router

TOKEN = os.environ.get("TOKEN") or os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Задайте TOKEN или BOT_TOKEN в окружении")


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include(start_router, echo_router)
    LongPolling(dp).run(bot)


if __name__ == "__main__":
    main()
