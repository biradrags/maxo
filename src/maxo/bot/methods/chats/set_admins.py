from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Path
from maxo.omit import Omittable, Omitted
from maxo.types.chat_admin import ChatAdmin
from maxo.types.simple_query_result import SimpleQueryResult


class SetAdmins(MaxoMethod[SimpleQueryResult]):
    """
    Назначить администратора группового чата

    Возвращает значение `true`, если в групповой чат добавлены все администраторы 

    Пример запроса:
    ```bash
    curl -X POST "https://platform-api.max.ru/chats/{chatId}/members/admins" \
      -H "Authorization: {access_token}" \
      -H "Content-Type: application/json" \
      -d '{
      "admins": [
        {
          "user_id": "{user_id}",
          "permissions": [
            "read_all_messages",
            "add_remove_members",
            "add_admins",
            "change_chat_info",
            "pin_message",
            "write"
          ],
          "alias": "Admin"
        }
      ]
    }'
    ```

    Args:
        admins: Список пользователей, которые получат права администратора чата
        chat_id: ID чата
        marker: Указатель на следующую страницу данных

    Источник: https://dev.max.ru/docs-api/methods/POST/chats/-chatId-/members/admins
    """

    __url__ = "chats/{chat_id}/members/admins"
    __method__ = "post"

    chat_id: Path[int]
    """ID чата"""

    admins: Body[list[ChatAdmin]]
    """Список пользователей, которые получат права администратора чата"""
    marker: Body[Omittable[int | None]] = Omitted()
    """Указатель на следующую страницу данных"""
