import pytest

from maxo import Dispatcher
from maxo.dialogs import (
    Dialog,
    DialogManager,
    StartMode,
    Window,
    setup_dialogs,
)
from maxo.dialogs.test_tools import BotClient, MockMessageManager
from maxo.dialogs.widgets.media.static import StaticMedia
from maxo.fsm.state import State, StatesGroup
from maxo.fsm.storages.memory import MemoryStorage
from maxo.routing.filters import Command
from maxo.types import Message


class MainSG(StatesGroup):
    with_url = State()
    with_path = State()


dialog = Dialog(
    Window(
        StaticMedia(url="fake_image.png"),
        state=MainSG.with_url,
    ),
    Window(
        StaticMedia(path="fake_image.png"),
        state=MainSG.with_path,
    ),
)


async def start_url(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainSG.with_url, mode=StartMode.RESET_STACK)


async def start_path(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainSG.with_path, mode=StartMode.RESET_STACK)


@pytest.mark.asyncio
async def test_click() -> None:
    dp = Dispatcher(
        storage=MemoryStorage(),
    )
    dp.include(dialog)
    dp.message_created.handler(start_url, Command("url"))
    dp.message_created.handler(start_path, Command("path"))

    client = BotClient(dp)
    message_manager = MockMessageManager()
    setup_dialogs(dp, message_manager=message_manager)

    # with url parameter
    await client.send("/url")
    first_message = message_manager.one_message()
    assert first_message.photo

    message_manager.reset_history()

    # with path parameter
    await client.send("/path")
    first_message = message_manager.one_message()
    assert first_message.photo
