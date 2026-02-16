from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body
from maxo.omit import Omittable, Omitted
from maxo.types.simple_query_result import SimpleQueryResult


class Subscribe(MaxoMethod[SimpleQueryResult]):
    """
    Подписка на обновления

    Подписывает бота на получение обновлений через WebHook. После вызова этого метода бот будет получать уведомления о новых событиях в чатах на указанный URL.
    Ваш сервер **должен** прослушивать один из следующих портов: `80`, `8080`, `443`, `8443`, `16384`-`32383`

    Пример запроса:
    ```bash
    curl -X POST "https://platform-api.max.ru/subscriptions" \
      -H "Authorization: {access_token}" \
      -H "Content-Type: application/json" \
      -d '{
      "url": "https://your-domain.com/webhook",
      "update_types": ["message_created", "bot_started"],
      "secret": "your_secret"
    }'
    ```

    Args:
        secret: Cекрет, который должен быть отправлен в заголовке `X-Max-Bot-Api-Secret` в каждом запросе Webhook. Разрешены только символы `A-Z`, `a-z`, `0-9`, и дефис. Заголовок рекомендован, чтобы запрос поступал из установленного веб-узла
        update_types: Список типов обновлений, которые ваш бот хочет получать. Для полного списка типов см. объект [Update](https://dev.max.ru/docs-api/objects/Update)
        url: URL HTTP(S)-эндпойнта вашего бота. Должен начинаться с `http(s)://`

    Источник: https://dev.max.ru/docs-api/methods/POST/subscriptions
    """

    __url__ = "subscriptions"
    __method__ = "post"

    url: Body[str]
    """URL HTTP(S)-эндпойнта вашего бота. Должен начинаться с `http(s)://`"""
    secret: Body[Omittable[str]] = Omitted()
    """Cекрет, который должен быть отправлен в заголовке `X-Max-Bot-Api-Secret` в каждом запросе Webhook. Разрешены только символы `A-Z`, `a-z`, `0-9`, и дефис. Заголовок рекомендован, чтобы запрос поступал из установленного веб-узла"""
    update_types: Body[Omittable[list[str]]] = Omitted()
    """Список типов обновлений, которые ваш бот хочет получать. Для полного списка типов см. объект [Update](https://dev.max.ru/docs-api/objects/Update)"""
