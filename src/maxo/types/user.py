from datetime import datetime

from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class User(MaxoType):
    """
    Объект, описывающий один из вариантов наследования:

    - [`User`](/docs-api/objects/User) — объект содержит общую информацию о пользователе или боте без аватара
    - [`UserWithPhoto`](/docs-api/objects/UserWithPhoto) — объект с общей информацией о пользователе или боте, дополнительно содержит URL аватара и описание
    - [`BotInfo`](/docs-api/objects/BotInfo) — объект включает общую информацию о боте, URL аватара и описание. Дополнительно содержит список команд, поддерживаемых ботом. Возвращается только при вызове метода [`GET /me`](/docs-api/methods/GET/me)
    - [`ChatMember`](/docs-api/objects/ChatMember) — объект включает общую информацию о пользователе или боте, URL аватара и описание при его наличии. Дополнительно содержит данные для пользователей-участников чата. Возвращается только при вызове некоторых методов группы `/chats`, например [`GET /chats/{chatId}/members`](/docs-api/methods/GET/chats/-chatId-/members)
    """

    first_name: str
    is_bot: bool
    last_activity_time: datetime
    user_id: int

    last_name: str | None = None
    username: str | None = None

    name: Omittable[str | None] = Omitted()

    @property
    def id(self) -> int:
        return self.user_id

    @property
    def fullname(self) -> str | None:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        return None
