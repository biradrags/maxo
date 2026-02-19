import tempfile
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from maxo import Bot, Dispatcher
from maxo.dialogs import Dialog, DialogManager, StartMode, Window, setup_dialogs
from maxo.dialogs.api.entities import (
    NewMessage,
    OldMessage,
)
from maxo.dialogs.api.protocols import MessageManagerProtocol
from maxo.dialogs.context.media_storage import MediaIdStorage
from maxo.dialogs.test_tools import BotClient
from maxo.dialogs.test_tools.memory_storage import JsonMemoryStorage
from maxo.dialogs.widgets.media import StaticMedia
from maxo.enums import AttachmentType, ChatType
from maxo.fsm import State, StatesGroup
from maxo.fsm.key_builder import DefaultKeyBuilder
from maxo.routing.filters import Command
from maxo.types import Message, PhotoAttachment, PhotoAttachmentPayload, Recipient


class MainSG(StatesGroup):
    start = State()


async def start(message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainSG.start, mode=StartMode.RESET_STACK)


class MockMessageManager(MessageManagerProtocol):
    def __init__(self):
        self.show_message_mock = AsyncMock()

    async def show_message(
        self,
        bot: Bot,
        new_message: NewMessage,
        old_message: OldMessage | None,
    ) -> OldMessage:
        await self.show_message_mock(bot, new_message, old_message)
        return OldMessage(
            recipient=Recipient(chat_id=1, user_id=1, chat_type=ChatType.CHAT),
            message_id="1",
            sequence_id=1,
            text=None,
            attachments=[
                PhotoAttachment(
                    payload=PhotoAttachmentPayload(
                        photo_id=123,
                        token="test_token",
                        url="https://example.com/photo.jpg",
                    ),
                ),
            ],
        )

    async def remove_kbd(self, bot, old_message, show_mode) -> None:
        pass

    async def answer_callback(self, bot, callback) -> None:
        pass


@pytest.mark.asyncio
async def test_media_id_storage_integration():
    media_storage = MediaIdStorage()
    message_manager = MockMessageManager()

    with tempfile.NamedTemporaryFile(suffix=".jpg") as f:
        path = Path(f.name)
        dialog = Dialog(
            Window(
                StaticMedia(path=path, type=AttachmentType.IMAGE),
                state=MainSG.start,
            ),
        )

        dp = Dispatcher(
            storage=JsonMemoryStorage(),
            key_builder=DefaultKeyBuilder(with_destiny=True),
        )
        dp.include(dialog)
        dp.message_created.handler(start, Command("start"))
        setup_dialogs(
            dp,
            message_manager=message_manager,
            media_id_storage=media_storage,
        )

        client = BotClient(dp)

        # First show: save media id
        await client.send("/start")

        message_manager.show_message_mock.assert_called_once()
        first_call_args = message_manager.show_message_mock.call_args
        first_new_message: NewMessage = first_call_args.args[1]
        first_media_attachment_request = first_new_message.media
        assert first_media_attachment_request is not None
        assert first_media_attachment_request.media_id is not None
        assert first_media_attachment_request.media_id.token is None

        saved_media_id = await media_storage.get_media_id(
            path,
            None,
            AttachmentType.IMAGE,
        )
        assert saved_media_id is not None
        assert saved_media_id.token == "test_token"

        # Second show: use cached media id
        message_manager.show_message_mock.reset_mock()
        await client.send("/start")

        message_manager.show_message_mock.assert_called_once()
        second_call_args = message_manager.show_message_mock.call_args
        second_new_message: NewMessage = second_call_args.args[1]
        second_media_attachment_request = second_new_message.media
        assert second_media_attachment_request is not None
        assert second_media_attachment_request.media_id is not None
        assert second_media_attachment_request.media_id.token == saved_media_id.token
