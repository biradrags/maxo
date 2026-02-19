import random
from datetime import UTC, datetime
from uuid import uuid4

from maxo import Bot
from maxo.dialogs import ShowMode
from maxo.dialogs.api.entities import MediaAttachment, NewMessage, OldMessage
from maxo.dialogs.api.protocols import (
    MessageManagerProtocol,
    MessageNotModified,
)
from maxo.enums import AttachmentType, ChatType
from maxo.types import (
    Callback,
    InlineKeyboardAttachment,
    Keyboard,
    Message,
    MessageBody,
    PhotoAttachment,
    PhotoAttachmentPayload,
    Recipient,
)


def file_id(media: MediaAttachment) -> str:
    file_id_ = None
    if media.file_id:
        file_id_ = media.file_id.file_id
    return file_id_ or str(uuid4())


def file_unique_id(media: MediaAttachment) -> str:
    file_unique_id_ = None
    if media.file_id:
        file_unique_id_ = media.file_id.file_unique_id
    return file_unique_id_ or str(uuid4())


class MockMessageManager(MessageManagerProtocol):
    def __init__(self) -> None:
        self.answered_callbacks: set[str] = set()
        self.sent_messages = []
        self.last_message_id = 0

    def reset_history(self) -> None:
        self.sent_messages.clear()
        self.answered_callbacks.clear()

    def assert_one_message(self) -> None:
        assert len(self.sent_messages) == 1

    def last_message(self) -> Message:
        return self.sent_messages[-1]

    def first_message(self) -> Message:
        return self.sent_messages[0]

    def one_message(self) -> Message:
        self.assert_one_message()
        return self.first_message()

    async def remove_kbd(
        self,
        bot: Bot,
        show_mode: ShowMode,
        old_message: OldMessage | None,
    ) -> Message | None:
        if not old_message:
            return None
        if show_mode in (ShowMode.DELETE_AND_SEND, ShowMode.NO_UPDATE):
            return None
        assert isinstance(old_message, OldMessage)

        new_attachments = [
            attach
            for attach in old_message.attachments
            if attach.type != AttachmentType.INLINE_KEYBOARD
        ]

        message = Message(
            timestamp=datetime.now(UTC),
            recipient=Recipient(
                chat_type=ChatType.CHAT,
                chat_id=old_message.recipient.chat_id,
                user_id=old_message.recipient.chat_id,
            ),
            body=MessageBody(
                mid=old_message.message_id,
                seq=old_message.sequence_id,
                text=old_message.text,
                attachments=new_attachments,
            ),
        )
        self.sent_messages.append(message)
        return message

    async def answer_callback(
        self,
        bot: Bot,
        callback: Callback,
    ) -> None:
        self.answered_callbacks.add(callback.callback_id)

    def assert_answered(self, callback_id: str) -> None:
        assert callback_id in self.answered_callbacks

    async def show_message(
        self,
        bot: Bot,
        new_message: NewMessage,
        old_message: OldMessage | None,
    ) -> OldMessage:
        assert isinstance(new_message, NewMessage)
        assert isinstance(old_message, (OldMessage, type(None)))
        if new_message.show_mode is ShowMode.NO_UPDATE:
            raise MessageNotModified

        message_id = self.last_message_id + 1
        self.last_message_id = message_id

        converted_attachments = []
        for new_attachment in new_message.attachments:
            if new_attachment.type == AttachmentType.IMAGE:
                converted_attachments.append(
                    PhotoAttachment(
                        payload=PhotoAttachmentPayload(
                            photo_id=random.randint(1, 1_000_000),
                            token=new_attachment.file_id or str(uuid4()),
                            url=new_attachment.url,
                        ),
                    ),
                )
            elif new_attachment.type == AttachmentType.INLINE_KEYBOARD:
                converted_attachments.append(
                    InlineKeyboardAttachment(
                        payload=Keyboard(buttons=new_attachment.payload.buttons),
                    ),
                )
            else:
                converted_attachments.append(new_attachment)

        self.sent_messages.append(
            Message(
                sender=bot.state.info,
                recipient=new_message.recipient,
                timestamp=datetime.now(UTC),
                body=MessageBody(
                    mid=str(message_id),
                    seq=message_id,
                    text=new_message.text,
                    attachments=converted_attachments,
                ),
            ),
        )

        return OldMessage(
            message_id=str(message_id),
            sequence_id=message_id,
            recipient=new_message.recipient,
            text=new_message.text,
            attachments=converted_attachments,
        )
