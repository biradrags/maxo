from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.chat_members_list import ChatMembersList


class GetAdmins(MaxoMethod[ChatMembersList]):
    """
    Получение списка администраторов группового чата

    Возвращает список всех администраторов группового чата. Бот должен быть администратором в запрашиваемом чате

    Пример запроса:
    ```bash
    curl -X GET "https://platform-api.max.ru/chats/{chatId}/members/admins" \
      -H "Authorization: {access_token}"
    ```

    Args:
        chat_id: ID чата

    Источник: https://dev.max.ru/docs-api/methods/GET/chats/-chatId-/members/admins
    """

    __url__ = "chats/{chat_id}/members/admins"
    __method__ = "get"

    chat_id: Path[int]
    """ID чата"""
