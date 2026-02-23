from datetime import UTC, datetime

from adaptix import P, Retort, loader
from unihttp.serializers.adaptix import DEFAULT_RETORT

from maxo._internal._adaptix.concat_provider import concat_provider
from maxo._internal._adaptix.has_tag_provider import has_tag_provider
from maxo.bot.warming_up import WarmingUpType, warming_up_retort
from maxo.enums import (
    AttachmentRequestType,
    AttachmentType,
    ButtonType,
    MarkupElementType,
    UpdateType,
)
from maxo.routing.updates import (
    BotAddedToChat,
    BotRemovedFromChat,
    BotStarted,
    BotStopped,
    ChatTitleChanged,
    DialogCleared,
    DialogMuted,
    DialogRemoved,
    DialogUnmuted,
    MessageCallback,
    MessageCreated,
    MessageEdited,
    MessageRemoved,
    UserAddedToChat,
    UserRemovedFromChat,
)
from maxo.types import (
    AudioAttachment,
    AudioAttachmentRequest,
    CallbackButton,
    ContactAttachment,
    ContactAttachmentRequest,
    EmphasizedMarkup,
    FileAttachment,
    FileAttachmentRequest,
    InlineKeyboardAttachment,
    InlineKeyboardAttachmentRequest,
    LinkButton,
    LinkMarkup,
    LocationAttachment,
    LocationAttachmentRequest,
    MessageButton,
    MonospacedMarkup,
    OpenAppButton,
    PhotoAttachment,
    PhotoAttachmentRequest,
    RequestContactButton,
    RequestGeoLocationButton,
    ShareAttachment,
    ShareAttachmentRequest,
    StickerAttachment,
    StickerAttachmentRequest,
    StrikethroughMarkup,
    StrongMarkup,
    UnderlineMarkup,
    UserMentionMarkup,
    VideoAttachment,
    VideoAttachmentRequest,
)

TAG_PROVIDERS = concat_provider(
    # ---> UpdateType <---
    has_tag_provider(BotAddedToChat, "update_type", UpdateType.BOT_ADDED),
    has_tag_provider(BotRemovedFromChat, "update_type", UpdateType.BOT_REMOVED),
    has_tag_provider(BotStarted, "update_type", UpdateType.BOT_STARTED),
    has_tag_provider(BotStopped, "update_type", UpdateType.BOT_STOPPED),
    has_tag_provider(ChatTitleChanged, "update_type", UpdateType.CHAT_TITLE_CHANGED),
    has_tag_provider(DialogCleared, "update_type", UpdateType.DIALOG_CLEARED),
    has_tag_provider(DialogMuted, "update_type", UpdateType.DIALOG_MUTED),
    has_tag_provider(DialogRemoved, "update_type", UpdateType.DIALOG_REMOVED),
    has_tag_provider(DialogUnmuted, "update_type", UpdateType.DIALOG_UNMUTED),
    has_tag_provider(MessageCallback, "update_type", UpdateType.MESSAGE_CALLBACK),
    has_tag_provider(MessageCreated, "update_type", UpdateType.MESSAGE_CREATED),
    has_tag_provider(MessageEdited, "update_type", UpdateType.MESSAGE_EDITED),
    has_tag_provider(MessageRemoved, "update_type", UpdateType.MESSAGE_REMOVED),
    has_tag_provider(UserAddedToChat, "update_type", UpdateType.USER_ADDED),
    has_tag_provider(UserRemovedFromChat, "update_type", UpdateType.USER_REMOVED),
    # ---> AttachmentType <---
    has_tag_provider(AudioAttachment, "type", AttachmentType.AUDIO),
    has_tag_provider(ContactAttachment, "type", AttachmentType.CONTACT),
    has_tag_provider(FileAttachment, "type", AttachmentType.FILE),
    has_tag_provider(PhotoAttachment, "type", AttachmentType.IMAGE),
    has_tag_provider(InlineKeyboardAttachment, "type", AttachmentType.INLINE_KEYBOARD),
    has_tag_provider(LocationAttachment, "type", AttachmentType.LOCATION),
    has_tag_provider(ShareAttachment, "type", AttachmentType.SHARE),
    has_tag_provider(StickerAttachment, "type", AttachmentType.STICKER),
    has_tag_provider(VideoAttachment, "type", AttachmentType.VIDEO),
    # ---> MarkupElementType <---
    has_tag_provider(EmphasizedMarkup, "type", MarkupElementType.EMPHASIZED),
    has_tag_provider(LinkMarkup, "type", MarkupElementType.LINK),
    has_tag_provider(MonospacedMarkup, "type", MarkupElementType.MONOSPACED),
    has_tag_provider(
        StrikethroughMarkup,
        "type",
        MarkupElementType.STRIKETHROUGH,
    ),
    has_tag_provider(StrongMarkup, "type", MarkupElementType.STRONG),
    has_tag_provider(UnderlineMarkup, "type", MarkupElementType.UNDERLINE),
    has_tag_provider(UserMentionMarkup, "type", MarkupElementType.USER_MENTION),
    # ---> AttachmentRequestType <---
    has_tag_provider(PhotoAttachmentRequest, "type", AttachmentRequestType.IMAGE),
    has_tag_provider(VideoAttachmentRequest, "type", AttachmentRequestType.VIDEO),
    has_tag_provider(AudioAttachmentRequest, "type", AttachmentRequestType.AUDIO),
    has_tag_provider(FileAttachmentRequest, "type", AttachmentRequestType.FILE),
    has_tag_provider(StickerAttachmentRequest, "type", AttachmentRequestType.STICKER),
    has_tag_provider(ContactAttachmentRequest, "type", AttachmentRequestType.CONTACT),
    has_tag_provider(
        InlineKeyboardAttachmentRequest,
        "type",
        AttachmentRequestType.INLINE_KEYBOARD,
    ),
    has_tag_provider(LocationAttachmentRequest, "type", AttachmentRequestType.LOCATION),
    has_tag_provider(ShareAttachmentRequest, "type", AttachmentRequestType.SHARE),
    # ---> KeyboardButtonType <---
    has_tag_provider(CallbackButton, "type", ButtonType.CALLBACK),
    has_tag_provider(LinkButton, "type", ButtonType.LINK),
    has_tag_provider(
        RequestContactButton,
        "type",
        ButtonType.REQUEST_CONTACT,
    ),
    has_tag_provider(
        RequestGeoLocationButton,
        "type",
        ButtonType.REQUEST_GEO_LOCATION,
    ),
    has_tag_provider(
        OpenAppButton,
        "type",
        ButtonType.OPEN_APP,
    ),
    has_tag_provider(
        MessageButton,
        "type",
        ButtonType.MESSAGE,
    ),
)


def create_response_loader(warming_up: bool = True) -> Retort:
    retort = DEFAULT_RETORT.extend(
        recipe=[
            TAG_PROVIDERS,
            loader(P[datetime], lambda x: datetime.fromtimestamp(x / 1000, tz=UTC)),
        ],
    )
    if warming_up:
        retort = warming_up_retort(retort, warming_up=WarmingUpType.TYPES)
    return retort
