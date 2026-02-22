Обработчики и Аргументы
=======================

Обработчик (Handler) — это асинхронная функция, которая выполняется в ответ на входящее событие (Update), если оно прошло через все фильтры. Это конечная точка обработки логики вашего бота.

Регистрация
-----------

Обработчики регистрируются через декораторы на роутере или диспетчере. В декоратор можно передать один или несколько фильтров.

.. code-block:: python

    from maxo.routing.filters import Command

    @router.message_created(Command("start"))
    async def my_handler(update, ctx, facade):
        ...

Аргументы
---------

**maxo** автоматически внедряет аргументы в функцию-обработчик на основе их имен и типов. Основные доступные аргументы:

1.  **Объект обновления** (первый позиционный аргумент): Типизированный объект события, например `MessageCreated`, `MessageCallback`. Содержит все данные, пришедшие от API.
2.  `ctx: Ctx` — Контекст выполнения. Это словарь-подобный объект, который живет в рамках обработки одного обновления. В нем хранятся ссылки на `bot`, `update`, а также любые данные, добавленные мидлварями.
3.  `facade: ...Facade` — Удобная обертка над обновлением. Подробнее в разделе :doc:`facades`.

.. code-block:: python

    from maxo.routing.ctx import Ctx
    from maxo.utils.facades import MessageCreatedFacade
    from maxo.routing.updates.message_created import MessageCreated

    @router.message_created()
    async def echo(
        update: MessageCreated,
        ctx: Ctx,
        facade: MessageCreatedFacade,
    ):
        await facade.answer_text(update.message.body.text)

Dependency Injection (DI)
-------------------------

Вы можете передавать произвольные данные в обработчики через фильтры и мидлвари.

1.  **Через фильтры**: Если фильтр возвращает словарь (`dict`), эти данные будут добавлены в аргументы обработчика (`kwargs`).
2.  **Через мидлвари**: Мидлварь может изменить `ctx` или вызвать `handler(ctx, **kwargs)`, добавив новые аргументы.

.. code-block:: python

    # Пример фильтра, который возвращает данные пользователя
    class UserFilter(BaseFilter):
        async def __call__(self, update, ctx) -> dict | bool:
            user = await get_user_from_db(update.user_id)
            if user:
                return {"user": user} # Передаем user в обработчик
            return False

    @router.message_created(UserFilter())
    async def handler(update, user: User, ctx):
        # Аргумент user будет автоматически передан из фильтра
        await ctx.bot.send_message(user.id, f"Hello, {user.name}!")

Возвращаемые значения
---------------------

Обычно обработчики ничего не возвращают (`None`). Однако, вы можете вернуть специальные значения для управления потоком (например, `UNHANDLED` для пропуска обработки, хотя чаще для этого используются исключения `SkipHandler`).
