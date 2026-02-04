from enum import StrEnum


class UpdateType(StrEnum):
    """
    Объект`Update` представляет различные типы событий, произошедших в чате. См. его наследников

    > Чтобы получать события из группового чата или канала, назначьте бота администратором
    """

    BOT_ADDED = "bot_added"
    BOT_REMOVED = "bot_removed"
    BOT_STARTED = "bot_started"
    BOT_STOPPED = "bot_stopped"
    CHAT_TITLE_CHANGED = "chat_title_changed"
    DIALOG_CLEARED = "dialog_cleared"
    DIALOG_MUTED = "dialog_muted"
    DIALOG_REMOVED = "dialog_removed"
    DIALOG_UNMUTED = "dialog_unmuted"
    MESSAGE_CALLBACK = "message_callback"
    MESSAGE_CREATED = "message_created"
    MESSAGE_EDITED = "message_edited"
    MESSAGE_REMOVED = "message_removed"
    USER_ADDED = "user_added"
    USER_REMOVED = "user_removed"

    MESSAGE_CHAT_CREATED = "message_chat_created"  # ????
