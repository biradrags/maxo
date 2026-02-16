from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path, Query
from maxo.omit import Omittable, Omitted
from maxo.types.chat_members_list import ChatMembersList


class GetMembers(MaxoMethod[ChatMembersList]):
    """
    Получение участников группового чата

    Возвращает список участников группового чата

    Пример запроса:
    ```bash
    curl -X GET "https://platform-api.max.ru/chats/{chatId}/members" \
      -H "Authorization: {access_token}"
    ```

    Args:
        chat_id: ID чата
        count: Количество участников, которых нужно вернуть
        marker: Указатель на следующую страницу данных
        user_ids: Список ID пользователей, чье членство нужно получить. Когда этот параметр передан, параметры `count` и `marker` игнорируются

    Источник: https://dev.max.ru/docs-api/methods/GET/chats/-chatId-/members
    """

    __url__ = "chats/{chat_id}/members"
    __method__ = "get"

    chat_id: Path[int]
    """ID чата"""

    count: Query[Omittable[int]] = Omitted()
    """Количество участников, которых нужно вернуть"""
    marker: Query[Omittable[int]] = Omitted()
    """Указатель на следующую страницу данных"""
    user_ids: Query[Omittable[list[int] | None]] = Omitted()
    """Список ID пользователей, чье членство нужно получить. Когда этот параметр передан, параметры `count` и `marker` игнорируются"""
