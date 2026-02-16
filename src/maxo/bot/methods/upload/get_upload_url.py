from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.enums.upload_type import UploadType
from maxo.types.upload_endpoint import UploadEndpoint


class GetUploadUrl(MaxoMethod[UploadEndpoint]):
    """
    Загрузка файлов

    Возвращает URL для последующей загрузки файла

    > Параметр `type=photo` больше не поддерживается. Если вы использовали `type=photo` в ранее созданных интеграциях — замените его на `type=image`

    Поддерживаются два типа загрузки:
    - **Multipart upload** — более простой, но менее надёжный способ. В этом случае используется заголовок `Content-Type: multipart/form-data`. Этот способ имеет ограничения:
        - Максимальный размер файла: 4 ГБ
        - Можно загружать только один файл за раз
        - Невозможно перезапустить загрузку, если она была остановлена

        
    - **Resumable upload** — более надёжный способ, если заголовок `Content-Type` не равен `multipart/form-data`. Этот способ позволяет загружать файл частями и возобновить загрузку с последней успешно загруженной части в случае ошибок

    Пример получения ссылки для загрузки:

    ```bash
    curl -X POST "https://platform-api.max.ru/uploads?type=file" \
      -H "Authorization: {access_token}"
    ```

    Пример загрузки файла по полученному URL:

    ```bash
    curl -X POST "%UPLOAD_URL%" \
      -H "Authorization: {access_token}" \
      -F "data=@example.mp4"
    ```

    Пример использования cURL для загрузки файла (вариант multipart upload):

    ```shell
    curl -i -X POST \
      -H "Content-Type: multipart/form-data" \
      -F "data=@movie.pdf" "%UPLOAD_URL%"
    ```

    Где `%UPLOAD_URL%` — это URL из результата метода в примере cURL запроса

    **Для загрузки видео и аудио:**

    1. Когда получаем ссылку на загрузку видео или аудио (`POST /uploads` с `type` = `video` или `type` = `audio`), вместе с `url` в ответе приходит `token`, который нужно использовать в сообщении (когда формируете `body` с `attachments`) в `POST /messages`.

    2. После загрузки видео или аудио (по `url` из шага выше) сервер возвращает `retval`

    3. C этого момента можно использовать `token`, чтобы прикреплять вложение в сообщение бота

    Механика отличается от `type` = `image` | `file`, где `token` возвращается в ответе на загрузку изображения или файла

    ## Прикрепление медиа
    Медиафайлы прикрепляются к сообщениям поэтапно:

    1. Получите URL для загрузки медиафайлов
    2. Загрузите файл по полученному URL
    3. После успешной загрузки получите JSON-объект в ответе. Используйте этот объект для создания вложения. Структура вложения:
        - `type`: тип медиа (например, `"video"`)
        - `payload`: JSON-объект, который вы получили

    Пример для видео:
    1. Получите URL для загрузки:
    ```bash
    curl -X POST "https://platform-api.max.ru/uploads?type=video" \
      -H "Authorization: {access_token}"
    ```

    Ответ:
    ```json
    {
        "url": "https://vu.mycdn.me/upload.do…"
    }
    ```

    2. Загрузите видео по URL:

    ```bash
    curl -X POST \
      -H "Content-Type: multipart/form-data" \
      -F "data=@movie.mp4" \
      "https://vu.mycdn.me/upload.do?sig={signature}&expires={timestamp}"
    ```

    Ответ:
    ```json
    {
        "token": "_3Rarhcf1PtlMXy8jpgie8Ai_KARnVFYNQTtmIRWNh4"
    }
    ```

    3. Отправьте сообщение с вложением:

    ```json
    {
        "text": "Message with video",
        "attachments": [
            {
                "type": "video",
                "payload": {
                    "token": "_3Rarhcf1PtlMXy8jpgie8Ai_KARnVFYNQTtmIRWNh4"
                }
            }
        ]
    }
    ```

    ## Обработка файлов

    После успешной загрузки сервер обрабатывает файл. Файлы от нескольких мегабайт обрабатываются дольше 

    Если отправить сообщение с вложением сразу после загрузки, может возникнуть ошибка:

    ```json
    {
      "code": "attachment.not.ready",
      "message": "Key: errors.process.attachment.file.not.processed"
    }
    ```

    **Как избежать ошибки:**
    - После загрузки файла сделайте паузу перед отправкой сообщения
    - Если отправка не удалась, повторите попытку через некоторое время. Увеличивайте интервал с каждой попыткой
    - Загружайте часто используемые файлы заранее и переиспользуйте токен

    Args:
        type: Тип загружаемого файла. Возможные значения: `"image"`, `"video"`, `"audio"`, `"file"`

    Источник: https://dev.max.ru/docs-api/methods/POST/uploads
    """

    __url__ = "uploads"
    __method__ = "post"

    type: Query[UploadType]
    """Тип загружаемого файла. Возможные значения: `"image"`, `"video"`, `"audio"`, `"file"`"""
