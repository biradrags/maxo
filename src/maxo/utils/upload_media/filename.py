_FILENAME_ESCAPES = str.maketrans({'"': "%22", "\r": "%0D", "\n": "%0A"})


def encode_multipart_filename(file_name: str) -> str:
    """
    Имя файла для `filename=` в multipart-загрузке на сервер MAX.

    Multipart-парсер сервера не декодирует percent-encoding (символ `%`
    подменяется на `_`, и клиент видит `_D0_9E...` вместо кириллицы),
    поэтому имя уходит сырым UTF-8 - как его шлют curl, браузеры и
    официальный SDK MAX. Кодируются только `"`, CR и LF (%22 / %0D / %0A,
    как в OkHttp и браузерах): кавычка ломает quoted-string, а CRLF -
    инъекция заголовков part'а. Проверено живой пробой 2026-08-05.

    Заголовочный (resumable) путь сервер парсит другим кодом - там,
    наоборот, нужен percent-encoding без кавычек, см. `resumable_upload`.
    """
    return file_name.translate(_FILENAME_ESCAPES)
