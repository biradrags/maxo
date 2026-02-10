import asyncio
from contextvars import copy_context

from maxo import Bot, Dispatcher
from maxo.dialogs.api.entities import DialogUpdate, DialogUpdateEvent


class Updater:
    def __init__(self, dp: Dispatcher) -> None:
        if not isinstance(dp, Dispatcher):
            raise TypeError("Root router must be Dispatcher.")
        self.dp = dp

    async def notify(self, update: DialogUpdate, bot: Bot) -> None:
        def callback() -> None:
            asyncio.create_task(  # noqa: RUF006
                self._process_update(update, bot),
            )

        asyncio.get_running_loop().call_soon(callback, context=copy_context())

    async def _process_update(self, update: DialogUpdate, bot: Bot) -> None:
        await self.dp.feed_update(
            DialogUpdate(
                update=DialogUpdateEvent(
                    bot=bot,
                    sender=update.update.sender,
                    chat=update.update.chat,
                    **self.dp.workflow_data,
                ),
            ),
            bot,
        )
