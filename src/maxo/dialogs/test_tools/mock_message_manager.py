import random
from datetime import UTC, datetime
from uuid import uuid4

from maxo import Bot
from maxo.dialogs import ShowMode
from maxo.dialogs.api.entities import NewMessage, OldMessage
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


class MockMessageManager(MessageManagerProtocol):
    def __init__(self) -> None:
        self.answered_callbacks: set[str] = set()
        self.sent_messages = []
        self.last_message_id = 0
        self.show_message_calls = []

    def reset_history(self) -> None:
        self.sent_messages.clear()
        self.answered_callbacks.clear()
        self.show_message_calls.clear()

    def assert_one_message(self) -> None:
        assert len(self.sent_messages) == 1

    def last_message(self) -> Message:
        return self.sent_messages[-1]

    def first_message(self) -> Message:
        return self.sent_messages[0]

    def one_message(self) -> Message:
        self.assert_one_message()
        return self.first_message()

    def assert_show_message(
        self,
        text: str | None = None,
        attachments: list | None = None,
    ) -> None:
        assert len(self.show_message_calls) == 1
        new_message: NewMessage = self.show_message_calls[0][1]
        if text is not None:
            assert new_message.text == text
        if attachments is not None:
            assert len(new_message.attachments) == len(attachments)
            for new_att, expected_att in zip(new_message.attachments, attachments):
                assert new_att.type == expected_att.type
                assert new_att.path == expected_att.path
                assert new_att.url == expected_att.url
                assert new_att.media_id == expected_att.media_id

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
                user_id=old_message.recipient.user_id,
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
        self.show_message_calls.append((bot, new_message, old_message))
        assert isinstance(new_message, NewMessage)
        assert isinstance(old_message, (OldMessage, type(None)))
        if new_message.show_mode is ShowMode.NO_UPDATE:
            raise MessageNotModified
        if (
            old_message
            and new_message.text == old_message.text
            and new_message.media == old_message.media
            and new_message.keyboard == old_message.keyboard
        ):
            raise MessageNotModified

        message_id = self.last_message_id + 1
        self.last_message_id = message_id

        converted_attachments = []
        media = new_message.media
        if media and media.type == AttachmentType.IMAGE:
            converted_attachments.append(
                PhotoAttachment(
                    payload=PhotoAttachmentPayload(
                        photo_id=random.randint(1, 1_000_000),
                        token=(
                            media.media_id.token if media.media_id else str(uuid4())
                        ),
                        url=media.url,
                    ),
                ),
            )

        keyboard = new_message.keyboard
        if keyboard:
            converted_attachments.append(
                InlineKeyboardAttachment(payload=Keyboard(buttons=keyboard)),
            )

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
