from enum import StrEnum


class Intent(StrEnum):
    """Намерение кнопки"""

    DEFAULT = "default"
    NEGATIVE = "negative"
    POSITIVE = "positive"
