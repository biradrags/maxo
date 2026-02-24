Фильтры
=======

Фильтры в **maxo** позволяют отсеивать события, которые вы хотите обрабатывать. Это один из ключевых механизмов маршрутизации.
Вместо того чтобы писать один большой ``if/else`` внутри обработчика, вы декларируете условия срабатывания прямо в декораторе.

.. code-block:: python

    from maxo.routing.filters import Command
    from maxo.routing.updates.message_created import MessageCreated
    from maxo.routing.ctx import Ctx
    from maxo.utils.facades import MessageCreatedFacade

    @dispatcher.message_created(Command("start"))
    async def start(update: MessageCreated, ctx: Ctx, facade: MessageCreatedFacade):
        ...

Встроенные фильтры
------------------

**maxo** поставляется с набором готовых фильтров:

- ``Command`` – проверяет команду (например, ``/start`` или ``/help``).
- ``StateFilter`` – фильтрует по текущему состоянию FSM (например, ``StateFilter(MyStates.waiting_name)``).
- ``MagicFilter`` – инструмент для создания условий на лету (см. ниже).

Комбинирование (Логические операции)
------------------------------------

Вы можете комбинировать фильтры с помощью логических операторов ``&`` (И), ``|`` (ИЛИ) и ``~`` (НЕ).

.. code-block:: python

    from magic_filter import F

    from maxo.routing.filters import Command
    from maxo.routing.updates.message_created import MessageCreated
    from maxo.routing.ctx import Ctx
    from maxo.utils.facades import MessageCreatedFacade
    from maxo.integrations.magic_filter import MagicFilter

    # Обработка команды /admin ИЛИ сообщения с текстом "secret"
    @dispatcher.message_created(Command("admin") | MagicFilter(F.text == "secret"))
    async def admin_area(update: MessageCreated, ctx: Ctx, facade: MessageCreatedFacade):
        ...

Magic Filter
------------

Библиотека интегрирована с ``magic_filter``. Это позволяет писать выразительные условия прямо в коде, обращаясь к атрибутам обновления через объект ``F``.

.. code-block:: python

    from magic_filter import F

    from maxo.routing.updates.message_created import MessageCreated
    from maxo.routing.ctx import Ctx
    from maxo.utils.facades import MessageCreatedFacade
    from maxo.integrations.magic_filter import MagicFilter

    # Сработает, если текст сообщения равен "hello"
    @dispatcher.message_created(MagicFilter(F.text == "hello"))
    async def hello(update: MessageCreated, ctx: Ctx, facade: MessageCreatedFacade):
        ...

    # Сработает, если у отправителя имя "Kirill"
    @dispatcher.message_created(MagicFilter(F.message.sender.first_name == "Kirill"))
    async def kirill_handler(update: MessageCreated, ctx: Ctx, facade: MessageCreatedFacade):
        ...

Создание своих фильтров
-----------------------

Фильтр – это любой вызываемый объект (callable), принимающий ``update`` и возвращающий ``bool`` (или ``Awaitable[bool]``).
Также фильтр может вернуть словарь, который будет передан в аргументы обработчика (как dependency injection).

.. code-block:: python

    from maxo.routing.filters import BaseFilter
    from maxo.routing.updates.message_created import MessageCreated
    from maxo.routing.ctx import Ctx

    class MyFilter(BaseFilter[MessageCreated]):
        async def __call__(self, update: MessageCreated, ctx: Ctx) -> bool:
            return update.message.body.text == "foo"

Пример: фильтр с параметром и DI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Фильтр может принимать аргументы конструктора и возвращать словарь с данными, которые станут доступны обработчику:

.. code-block:: python

    from maxo.routing.filters import BaseFilter
    from maxo.routing.updates.message_created import MessageCreated
    from maxo.routing.ctx import Ctx

    class MinLengthFilter(BaseFilter[MessageCreated]):
        """Пропускает сообщения длиннее min_length символов."""

        def __init__(self, min_length: int):
            self.min_length = min_length

        async def __call__(self, update: MessageCreated, ctx: Ctx) -> bool | dict:
            text = update.message.body.text or ""
            if len(text) >= self.min_length:
                # Возвращаем словарь – значения попадут в аргументы обработчика
                return {"text_length": len(text)}
            return False

    @router.message_created(MinLengthFilter(10))
    async def long_message_handler(
        update: MessageCreated,
        ctx: Ctx,
        facade: MessageCreatedFacade,
        text_length: int,
    ):
        await facade.answer_text(f"Длинное сообщение! ({text_length} символов)")

