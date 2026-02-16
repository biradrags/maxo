from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.simple_query_result import SimpleQueryResult


class UnpinMessage(MaxoMethod[SimpleQueryResult]):
    """
    Удаление закреплённого сообщения в групповом чате

    Удаляет закреплённое сообщение в групповом чате

    Пример запроса:
    ```bash
    curl -X DELETE "https://platform-api.max.ru/chats/{chatId}/pin" \
      -H "Authorization: {access_token}"
    ```

    Args:
        chat_id: ID чата, из которого нужно удалить закреплённое сообщение

    Источник: https://dev.max.ru/docs-api/methods/DELETE/chats/-chatId-/pin
    """

    __url__ = "chats/{chat_id}/pin"
    __method__ = "delete"

    chat_id: Path[int]
    """ID чата, из которого нужно удалить закреплённое сообщение"""
