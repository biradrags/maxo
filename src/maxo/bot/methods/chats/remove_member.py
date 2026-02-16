from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path, Query
from maxo.omit import Omittable, Omitted
from maxo.types.simple_query_result import SimpleQueryResult


class RemoveMember(MaxoMethod[SimpleQueryResult]):
    """
    Удаление участника из группового чата

    Удаляет участника из группового чата. Для этого могут потребоваться дополнительные права

    Пример запроса:
    ```bash
    curl -X DELETE "https://platform-api.max.ru/chats/{chatId}/members?user_id={user_id}&block=true" \
      -H "Authorization: {access_token}"
    ```

    Args:
        block: Если установлено в `true`, пользователь будет заблокирован в чате. Применяется только для чатов с публичной или приватной ссылкой. Игнорируется в остальных случаях
        chat_id: ID чата
        user_id: ID пользователя, которого нужно удалить из чата

    Источник: https://dev.max.ru/docs-api/methods/DELETE/chats/-chatId-/members
    """

    __url__ = "chats/{chat_id}/members"
    __method__ = "delete"

    chat_id: Path[int]
    """ID чата"""

    user_id: Query[int]
    """ID пользователя, которого нужно удалить из чата"""
    block: Query[Omittable[bool]] = Omitted()
    """Если установлено в `true`, пользователь будет заблокирован в чате. Применяется только для чатов с публичной или приватной ссылкой. Игнорируется в остальных случаях"""
