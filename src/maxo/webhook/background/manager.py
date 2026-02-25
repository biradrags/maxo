from __future__ import annotations

import asyncio
from typing import Any

from maxo import loggers


class BackgroundTaskManager:
    def __init__(self) -> None:
        self._tasks: set[asyncio.Task[Any]] = set()

    def spawn(self, coro: Any) -> asyncio.Task[Any]:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._on_done)
        return task

    def _on_done(self, task: asyncio.Task[Any]) -> None:
        self._tasks.discard(task)
        if task.cancelled():
            return
        exc = task.exception()
        if exc is not None:
            loggers.webhook.error("Webhook background task failed", exc_info=exc)

    async def wait_all(self, timeout: float | None = 30.0) -> None:
        if not self._tasks:
            return
        tasks = tuple(self._tasks)
        if timeout is None:
            await asyncio.gather(*tasks, return_exceptions=True)
            return
        try:
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout=timeout,
            )
        except TimeoutError:
            for t in tasks:
                if not t.done():
                    t.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
