from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from maxo.dialogs.api.entities import ShowMode
from maxo.dialogs.api.entities.link_preview import LinkPreviewOptions
from maxo.enums import TextFormat
from maxo.types import (
    InlineKeyboardAttachmentRequest,
    NewMessageLink,
    Recipient,
)
from maxo.types.attachments import Attachments, AttachmentsRequests
from maxo.types.buttons import InlineButtons

MarkupVariant = list[list[InlineButtons]]


class UnknownText(Enum):
    UNKNOWN = object()


@dataclass
class OldMessage:
    recipient: Recipient
    message_id: str
    sequence_id: int
    text: str | None | UnknownText
    attachments: list[Attachments]


@dataclass
class NewMessage:
    recipient: Recipient
    attachments: list[AttachmentsRequests]
    parse_mode: TextFormat | None = None
    link_preview_options: LinkPreviewOptions | None = None
    show_mode: ShowMode = ShowMode.AUTO
    text: str | None = None
    link_to: NewMessageLink | None = None

    @property
    def keyboard(self) -> Sequence[Sequence[InlineButtons]]:
        if not self.attachments:
            return []
        for attachment in self.attachments:
            if isinstance(attachment, InlineKeyboardAttachmentRequest):
                return attachment.payload.buttons
        return []
