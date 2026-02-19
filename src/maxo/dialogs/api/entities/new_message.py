from enum import Enum

from maxo.dialogs.api.entities import MediaAttachment, ShowMode
from maxo.dialogs.api.entities.link_preview import LinkPreviewOptions
from maxo.enums import TextFormat
from maxo.types import (
    Attachments,
    InlineButtons,
    InlineKeyboardAttachment,
    MaxoType,
    MediaAttachments,
    NewMessageLink,
    Recipient,
)

MarkupVariant = list[list[InlineButtons]]


class UnknownText(Enum):
    UNKNOWN = object()


class OldMessage(MaxoType):
    recipient: Recipient
    message_id: str
    sequence_id: int
    text: str | None | UnknownText
    attachments: list[Attachments]

    @property
    def keyboard(self) -> MarkupVariant | None:
        for attachment in self.attachments:
            if isinstance(attachment, InlineKeyboardAttachment):
                return attachment.payload.buttons
        return None

    @property
    def media(self) -> MediaAttachments | None:
        for attachment in self.attachments:
            if isinstance(attachment, MediaAttachments):
                return attachment
        return None


class NewMessage(MaxoType):
    recipient: Recipient
    keyboard: MarkupVariant | None = None
    media: MediaAttachment | None = None
    parse_mode: TextFormat | None = None
    link_preview_options: LinkPreviewOptions | None = None
    show_mode: ShowMode = ShowMode.AUTO
    text: str | None = None
    link_to: NewMessageLink | None = None
