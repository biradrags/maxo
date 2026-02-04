from enum import StrEnum


class ChatAdminPermission(StrEnum):
    """Права администратора чата"""

    ADD_ADMINS = "add_admins"
    ADD_REMOVE_MEMBERS = "add_remove_members"
    CAN_CALL = "can_call"
    CHANGE_CHAT_INFO = "change_chat_info"
    DELETE_MESSAGE = "delete_message"
    EDIT_LINK = "edit_link"
    EDIT_MESSAGE = "edit_message"
    PIN_MESSAGE = "pin_message"
    POST_EDIT_DELETE_MESSAGE = "post_edit_delete_message"
    READ_ALL_MESSAGES = "read_all_messages"
    WRITE = "write"
