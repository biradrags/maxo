=======================
Настройка и Интеграции
=======================

Настройка
=========

Чтобы система диалогов работала корректно, необходимо инициализировать её после регистрации всех ваших диалогов в диспетчере (роутере).

.. code-block:: python

    from maxo.dialogs import setup_dialogs
    from maxo import Dispatcher

    dp = Dispatcher()
    # ... подключение роутеров и диалогов ...

    # Инициализация (регистрирует фоновые процессоры, мидлвари диалогов)
    setup_dialogs(dp)

Фоновый менеджер (Background Manager)
=====================================

В обычных хэндлерах ``DialogManager`` передается в качестве аргумента автоматически. Но иногда вам нужно обновить диалог из фоновой задачи (например, по таймеру или из Celery/Redis/Taskiq). Для этого используется ``BgManagerFactory``.

Фабрика автоматически добавляется в параметры вызова, если вы используете DI. С её помощью можно получить менеджер для конкретного чата и пользователя.

.. code-block:: python

    from maxo.dialogs.api.protocols import BgManagerFactory

    async def background_job(bg_factory: BgManagerFactory, chat_id: int, user_id: int):
        manager = bg_factory.bg(chat_id=chat_id, user_id=user_id)
        # запуск нового диалога
        await manager.start(SG.main)
        # или просто обновление UI
        await manager.update({"status": "completed"})
