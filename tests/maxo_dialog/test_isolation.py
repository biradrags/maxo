import asyncio
from asyncio import Event

import pytest

from maxo import Dispatcher
from maxo.dialogs import setup_dialogs
from maxo.dialogs.test_tools import BotClient, MockMessageManager
from maxo.dialogs.test_tools.memory_storage import JsonMemoryStorage
from maxo.routing.filters import CommandStart
from maxo.types import Message


async def start(
    _message: Message,
    data: list,
    event_common: Event,
) -> None:
    data.append(1)
    await event_common.wait()


@pytest.mark.asyncio
@pytest.mark.repeat(10)
async def test_concurrent_events() -> None:
    event_common = Event()
    data = []
    dp = Dispatcher(
        workflow_data={"event_common": event_common, "data": data},
        storage=JsonMemoryStorage(),
    )
    dp.message_created.handler(start, CommandStart())

    client = BotClient(dp)
    message_manager = MockMessageManager()
    setup_dialogs(dp, message_manager=message_manager)

    # start
    t1 = asyncio.create_task(client.send("/start"))
    t2 = asyncio.create_task(client.send("/start"))
    await asyncio.sleep(0.1)
    assert len(data) == 1  # "Only single event expected to be processed"
    event_common.set()
    await t1
    await t2
    assert len(data) == 2
