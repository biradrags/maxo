from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.types.simple_query_result import SimpleQueryResult


class Unsubscribe(MaxoMethod[SimpleQueryResult]):
    """
    Отписка от обновлений

    Отписывает бота от получения обновлений через Webhook. После вызова этого метода бот перестаёт получать уведомления о новых событиях, и становится доступна доставка уведомлений через API с длительным опросом

    Пример запроса:
    ```bash
    curl -X DELETE "https://platform-api.max.ru/subscriptions?url=https://your-domain.com/webhook" \
      -H "Authorization: {access_token}"
    ```

    Args:
        url: URL, который нужно удалить из подписок на WebHook

    Источник: https://dev.max.ru/docs-api/methods/DELETE/subscriptions
    """

    __url__ = "subscriptions"
    __method__ = "delete"

    url: Query[str]
    """URL, который нужно удалить из подписок на WebHook"""
