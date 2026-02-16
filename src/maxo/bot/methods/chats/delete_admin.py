from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.simple_query_result import SimpleQueryResult


class DeleteAdmin(MaxoMethod[SimpleQueryResult]):
    """
    Отменить права администратора в групповом чате

    Отменяет права администратора у пользователя в групповом чате, лишая его административных привилегий

    Пример запроса:
    ```bash
    curl -X DELETE "https://platform-api.max.ru/chats/{chatId}/members/admins/{userId}" \
      -H "Authorization: {access_token}"
    ```

    Args:
        chat_id: ID чата
        user_id: Идентификатор пользователя

    Источник: https://dev.max.ru/docs-api/methods/DELETE/chats/-chatId-/members/admins/-userId-
    """

    __url__ = "chats/{chat_id}/members/admins/{user_id}"
    __method__ = "delete"

    chat_id: Path[int]
    """ID чата"""
    user_id: Path[int]
    """Идентификатор пользователя"""
