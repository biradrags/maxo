from enum import StrEnum


class MessageLinkType(StrEnum):
    """Тип связанного сообщения"""

    FORWARD = "forward"
    REPLY = "reply"
