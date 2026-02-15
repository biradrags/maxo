from typing import Any

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
from maxo.dialogs.test_tools.memory_storage import JsonMemoryStorage
from maxo.dialogs.widgets.text import Format
from maxo.fsm.state import State, StatesGroup
from maxo.routing.filters import CommandStart

# from maxo.types import ChatMemberMember, ChatMemberOwner


class MainSG(StatesGroup):
    start = State()


window = Window(
    Format("stub"),
    state=MainSG.start,
)


async def start(event: Any, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainSG.start, mode=StartMode.RESET_STACK)


@pytest.fixture
def message_manager() -> MockMessageManager:
    return MockMessageManager()


@pytest.fixture
def dp(message_manager) -> Dispatcher:
    dp = Dispatcher(storage=JsonMemoryStorage())
    dp.include(Dialog(window))
    setup_dialogs(dp, message_manager=message_manager)
    return dp


@pytest.fixture
def client(dp) -> BotClient:
    return BotClient(dp)


@pytest.mark.asyncio
async def test_click(dp, client, message_manager) -> None:
    dp.message_created.handler(start, CommandStart())
    await client.send("/start")
    first_message = message_manager.one_message()
    assert first_message.text == "stub"


@pytest.mark.asyncio
async def test_request_join(dp, client, message_manager) -> None:
    dp.user_added_to_chat.handler(start)
    await client.request_chat_join()
    first_message = message_manager.one_message()
    assert first_message.text == "stub"


# TODO: Fix
@pytest.mark.asyncio
async def test_my_chat_member_update(dp, client, message_manager) -> None:
    dp.bot_added_to_chat.handler(start)
    await client.my_chat_member_update(
        ChatMemberMember(user=client.user),
        ChatMemberOwner(user=client.user, is_anonymous=False),
    )
    first_message = message_manager.one_message()
    assert first_message.text == "stub"
