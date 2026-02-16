from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Path
from maxo.types.simple_query_result import SimpleQueryResult


class AddMembers(MaxoMethod[SimpleQueryResult]):
    """
    Добавление участников в групповой чат

    Добавляет участников в групповой чат. Для этого могут потребоваться дополнительные права

    Пример запроса:
    ```bash
    curl -X POST "https://platform-api.max.ru/chats/{chatId}/members" \
      -H "Authorization: {access_token}" \
      -H "Content-Type: application/json" \
      -d '{
      "user_ids": ["{user_id_1}", "{user_id_2}"]
    }'
    ```

    Args:
        chat_id: ID чата
        user_ids: 

    Источник: https://dev.max.ru/docs-api/methods/POST/chats/-chatId-/members
    """

    __url__ = "chats/{chat_id}/members"
    __method__ = "post"

    chat_id: Path[int]
    """ID чата"""

    user_ids: Body[list[int]]
