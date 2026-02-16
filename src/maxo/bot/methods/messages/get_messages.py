from datetime import datetime

from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.omit import Omittable, Omitted
from maxo.types.message_list import MessageList


class GetMessages(MaxoMethod[MessageList]):
    """
    Получение сообщений

    Метод возвращает информацию о сообщении или массив сообщений из чата. Для выполнения запроса нужно указать один из параметров — `chat_id` или `message_ids`:

    - `chat_id` — метод возвращает массив сообщений из указанного чата. Сообщения возвращаются в обратном порядке: последние сообщения будут первыми в массиве

    - `message_ids` — метод возвращает информацию о запрошенных сообщениях. Можно указать один идентификатор или несколько

    Пример запроса с использованием `chat_id`:
    ```bash
    curl -X GET "https://platform-api.max.ru/messages?chat_id={chat_id}" \
      -H "Authorization: {access_token}"
    ```

    Пример запроса с использованием `message_ids`:
    ```bash
    curl -X GET "https://platform-api.max.ru/messages?message_ids={message_id1},{message_id2}" \
      -H "Authorization: {access_token}"
    ```

    Args:
        chat_id: ID чата, чтобы получить сообщения из определённого чата. Обязательный параметр, если не указан `message_ids`
        count: Максимальное количество сообщений в ответе
        from_: Время начала для запрашиваемых сообщений (в формате Unix timestamp)
        message_ids: Список ID сообщений, которые нужно получить (через запятую). Обязательный параметр, если не указан `chat_id`
        to: Время окончания для запрашиваемых сообщений (в формате Unix timestamp)

    Источник: https://dev.max.ru/docs-api/methods/GET/messages
    """

    __url__ = "messages"
    __method__ = "get"

    chat_id: Query[Omittable[int]] = Omitted()
    """ID чата, чтобы получить сообщения из определённого чата. Обязательный параметр, если не указан `message_ids`"""
    count: Query[Omittable[int]] = Omitted()
    """Максимальное количество сообщений в ответе"""
    from_: Query[Omittable[datetime]] = Omitted()
    """Время начала для запрашиваемых сообщений (в формате Unix timestamp)"""
    message_ids: Query[Omittable[list[str] | None]] = Omitted()
    """Список ID сообщений, которые нужно получить (через запятую). Обязательный параметр, если не указан `chat_id`"""
    to: Query[Omittable[datetime]] = Omitted()
    """Время окончания для запрашиваемых сообщений (в формате Unix timestamp)"""
