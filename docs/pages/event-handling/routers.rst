Диспетчер и Роутеры
===================

В основе обработки событий в **maxo** лежит механизм маршрутизации, который позволяет гибко управлять потоком входящих обновлений.

Диспетчер (Dispatcher)
----------------------

`Dispatcher` — это корневой роутер и «сердце» вашего бота. Он отвечает за получение обновлений (через Long Polling или Webhook) и их распределение по цепочке обработчиков. Диспетчер также инициализирует хранилище состояний (FSM) и глобальные middleware.

.. code-block:: python

    from maxo import Dispatcher, Bot
    from maxo.utils.long_polling import LongPolling

    bot = Bot(token="...")
    dispatcher = Dispatcher()
    
    # Регистрация обработчиков прямо в диспетчере (так как он тоже Router)
    @dispatcher.message_created()
    async def echo(update, ctx, facade):
        ...
    
    # Запуск
    LongPolling(dispatcher).run(bot)

Роутеры (Routers)
-----------------

`Router` позволяет структурировать код бота, разбивая его на логические модули (например, «админка», «магазин», «техподдержка»). Вместо того чтобы регистрировать все обработчики в одном файле, вы можете разнести их по разным роутерам.

Вы можете создавать сколько угодно роутеров и вкладывать их друг в друга. Событие проходит по роутерам в порядке их регистрации.

.. code-block:: python

    from maxo import Router

    admin_router = Router(name="admin")
    shop_router = Router(name="shop")

    # Регистрация обработчиков в роутерах
    @admin_router.message_created(...)
    async def admin_handler(...): ...

    @shop_router.message_created(...)
    async def shop_handler(...): ...

    # Подключение роутеров к диспетчеру
    dispatcher.include(admin_router)
    dispatcher.include(shop_router)

Вложенность
-----------

Роутеры могут быть вложенными. Это позволяет создавать сложные иерархии обработки. Например, у вас может быть главный роутер для диалогов, который включает в себя под-роутеры для разных сценариев.

.. code-block:: python

    settings_router = Router()
    profile_router = Router()
    
    # Роутер профиля включает в себя роутер настроек
    profile_router.include(settings_router)
    
    # Диспетчер включает роутер профиля
    dispatcher.include(profile_router)

Порядок обработки
-----------------

Когда приходит событие (например, новое сообщение), оно проверяется на соответствие фильтрам обработчиков в каждом роутере по очереди:

1.  Сначала проверяются обработчики `dispatcher`.
2.  Затем проверяются вложенные роутеры в том порядке, в котором они были подключены через `include()`.
3.  Внутри каждого роутера обработчики проверяются в порядке их определения в коде.

Если обработчик найден и все фильтры прошли успешно, событие обрабатывается, и дальнейшее распространение останавливается.
Если ни один обработчик в текущем роутере не подошел, управление передается следующему роутеру в списке.

Доступные события
-----------------

Ниже приведен список всех событий, которые вы можете перехватывать и обрабатывать с помощью диспетчера и роутеров.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Декоратор регистрации
     - Тип события (Update)
     - Описание
   * - ``@router.message_created``
     - :class:`~maxo.routing.updates.message_created.MessageCreated`
     - Новое сообщение от пользователя (текст, фото, файлы и т.д.).
   * - ``@router.message_callback``
     - :class:`~maxo.routing.updates.message_callback.MessageCallback`
     - Нажатие на кнопку Inline-клавиатуры.
   * - ``@router.message_edited``
     - :class:`~maxo.routing.updates.message_edited.MessageEdited`
     - Пользователь отредактировал ранее отправленное сообщение.
   * - ``@router.message_removed``
     - :class:`~maxo.routing.updates.message_removed.MessageRemoved`
     - Пользователь удалил сообщение.
   * - ``@router.bot_started``
     - :class:`~maxo.routing.updates.bot_started.BotStarted`
     - Пользователь нажал кнопку «Запустить» или впервые начал диалог с ботом.
   * - ``@router.bot_stopped``
     - :class:`~maxo.routing.updates.bot_stopped.BotStopped`
     - Пользователь заблокировал бота.
   * - ``@router.user_added_to_chat``
     - :class:`~maxo.routing.updates.user_added_to_chat.UserAddedToChat`
     - В групповой чат добавлен новый участник.
   * - ``@router.user_removed_from_chat``
     - :class:`~maxo.routing.updates.user_removed_from_chat.UserRemovedFromChat`
     - Участник покинул групповой чат или был удален.
   * - ``@router.bot_added_to_chat``
     - :class:`~maxo.routing.updates.bot_added_to_chat.BotAddedToChat`
     - Бот добавлен в групповой чат.
   * - ``@router.bot_removed_from_chat``
     - :class:`~maxo.routing.updates.bot_removed_from_chat.BotRemovedFromChat`
     - Бот удален из группового чата.
   * - ``@router.chat_title_changed``
     - :class:`~maxo.routing.updates.chat_title_changed.ChatTitleChanged`
     - Название группового чата изменено.
   * - ``@router.dialog_cleared``
     - :class:`~maxo.routing.updates.dialog_cleared.DialogCleared`
     - История переписки очищена.
   * - ``@router.dialog_removed``
     - :class:`~maxo.routing.updates.dialog_removed.DialogRemoved`
     - Диалог удален.
   * - ``@router.dialog_muted`` / ``@router.dialog_unmuted``
     - :class:`~maxo.routing.updates.dialog_muted.DialogMuted` / :class:`~maxo.routing.updates.dialog_unmuted.DialogUnmuted`
     - Уведомления в диалоге отключены или включены.
   * - ``@router.error``
     - :class:`~maxo.routing.updates.error.ErrorEvent`
     - Произошла ошибка при обработке другого события.

Сигналы жизненного цикла
~~~~~~~~~~~~~~~~~~~~~~~~

Эти события не приходят от сервера MAX/API, а генерируются самим фреймворком при запуске и остановке.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Декоратор регистрации
     - Тип сигнала
     - Описание
   * - ``@router.before_startup``
     - :class:`~maxo.routing.signals.startup.BeforeStartup`
     - Вызывается перед запуском процесса получения обновлений (Polling/Webhook).
   * - ``@router.after_startup``
     - :class:`~maxo.routing.signals.startup.AfterStartup`
     - Вызывается сразу после успешного старта.
   * - ``@router.before_shutdown``
     - :class:`~maxo.routing.signals.shutdown.BeforeShutdown`
     - Вызывается перед началом процесса остановки бота (Graceful Shutdown).
   * - ``@router.after_shutdown``
     - :class:`~maxo.routing.signals.shutdown.AfterShutdown`
     - Вызывается после полной остановки и закрытия соединений.
