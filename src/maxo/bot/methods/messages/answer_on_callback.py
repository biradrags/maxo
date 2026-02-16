from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Query
from maxo.omit import Omittable, Omitted
from maxo.types.new_message_body import NewMessageBody
from maxo.types.simple_query_result import SimpleQueryResult


class AnswerOnCallback(MaxoMethod[SimpleQueryResult]):
    """
    Ответ на callback

    Этот метод используется для отправки ответа после того, как пользователь нажал на кнопку. Ответом может быть обновленное сообщение и/или одноразовое уведомление для пользователя

    Пример запроса:
    ```bash
    curl -X POST "https://platform-api.max.ru/answers?callback_id=callback_id" \
      -H "Authorization: {access_token}" \
      -H "Content-Type: application/json" \
      -d '{
        "message": {
          "text": "Это сообщение с кнопкой-ссылкой",
          "attachments": [
            {
              "type": "inline_keyboard",
              "payload": {
                "buttons": [
                  [
                    {
                      "type": "link",
                      "text": "Откройте сайт",
                      "url": "https://example.com"
                    }
                  ]
                ]
              }
            }
          ]
        }
      }'
    ```

    Args:
        callback_id: Идентификатор кнопки, по которой пользователь кликнул. Бот получает идентификатор как часть [Update](https://dev.max.ru/docs-api/objects/Update) с типом`message_callback`.
            Можно получить из [GET:/updates](https://dev.max.ru/docs-api/methods/GET/updates) через поле `updates[i].callback.callback_id`
        message: Заполните это, если хотите изменить текущее сообщение
        notification: Заполните это, если хотите просто отправить одноразовое уведомление пользователю

    Источник: https://dev.max.ru/docs-api/methods/POST/answers
    """

    __url__ = "answers"
    __method__ = "post"

    callback_id: Query[str]
    """
    Идентификатор кнопки, по которой пользователь кликнул. Бот получает идентификатор как часть [Update](https://dev.max.ru/docs-api/objects/Update) с типом`message_callback`.

    Можно получить из [GET:/updates](https://dev.max.ru/docs-api/methods/GET/updates) через поле `updates[i].callback.callback_id`
    """

    message: Body[Omittable[NewMessageBody | None]] = Omitted()
    """Заполните это, если хотите изменить текущее сообщение"""
    notification: Body[Omittable[str | None]] = Omitted()
    """Заполните это, если хотите просто отправить одноразовое уведомление пользователю"""
