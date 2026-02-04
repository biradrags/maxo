from datetime import datetime

from maxo.enums.chat_admin_permission import ChatAdminPermission
from maxo.types.user_with_photo import UserWithPhoto


class ChatMember(UserWithPhoto):
    """Объект включает общую информацию о пользователе или боте, URL аватара и описание (при наличии). Дополнительно содержит данные для пользователей-участников чата. Возвращается только при вызове некоторых методов группы `/chats`, например [`GET /chats/{chatId}/members`](/docs-api/methods/GET/chats/-chatId-/members)"""

    alias: str
    is_admin: bool
    is_owner: bool
    join_time: datetime
    last_access_time: datetime

    permissions: list[ChatAdminPermission] | None = None
