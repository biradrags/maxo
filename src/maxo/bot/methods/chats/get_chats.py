from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.omit import Omittable, Omitted
from maxo.types.chat_list import ChatList


class GetChats(MaxoMethod[ChatList]):
    """
    Получение списка всех групповых чатов

    Возвращает список групповых чатов, в которых участвовал бот, информацию о каждом чате и маркер для перехода к следующей странице списка

    Пример запроса:
    ```bash
    curl -X GET "https://platform-api.max.ru/chats" \
      -H "Authorization: {access_token}"
    ```

    Args:
        count: Количество запрашиваемых чатов
        marker: Указатель на следующую страницу данных. Для первой страницы передайте `null`

    Источник: https://dev.max.ru/docs-api/methods/GET/chats
    """

    __url__ = "chats"
    __method__ = "get"

    count: Query[Omittable[int]] = Omitted()
    """Количество запрашиваемых чатов"""
    marker: Query[Omittable[int]] = Omitted()
    """Указатель на следующую страницу данных. Для первой страницы передайте `null`"""
