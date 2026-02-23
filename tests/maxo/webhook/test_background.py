import asyncio
import logging
from unittest.mock import MagicMock

import pytest

from maxo.webhook.background import BackgroundTaskManager


@pytest.mark.asyncio
async def test_spawn_and_wait_all() -> None:
    manager = BackgroundTaskManager()
    done = asyncio.Event()

    async def task() -> None:
        await done.wait()

    manager.spawn(task())
    close = asyncio.create_task(manager.wait_all())
    await asyncio.sleep(0)
    assert not close.done()
    done.set()
    await close


@pytest.mark.asyncio
async def test_exception_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.ERROR, logger="maxo.webhook")
    manager = BackgroundTaskManager()

    async def failing() -> None:
        raise RuntimeError("boom")

    manager.spawn(failing())
    await manager.wait_all()
    assert "Webhook background task failed" in caplog.text


@pytest.mark.asyncio
async def test_wait_all_cancels_hung_tasks() -> None:
    manager = BackgroundTaskManager()
    hung = asyncio.Event()

    async def never_ends() -> None:
        await hung.wait()

    manager.spawn(never_ends())
    await manager.wait_all(timeout=0.05)
    hung.set()
    assert not manager._tasks


@pytest.mark.asyncio
async def test_wait_all_with_cancellation_does_not_raise() -> None:
    manager = BackgroundTaskManager()
    gate = asyncio.Event()

    async def cancelled_soon() -> None:
        await gate.wait()

    manager.spawn(cancelled_soon())
    await manager.wait_all(timeout=0.01)
    gate.set()
