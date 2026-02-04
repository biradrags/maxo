from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class BotCommand(MaxoType):
    """до 32 элементов<br/>Команды, поддерживаемые ботом"""

    name: str

    description: Omittable[str | None] = Omitted()
