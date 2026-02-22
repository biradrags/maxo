Состояния (FSM)
===============

Конечный автомат (Finite State Machine, FSM) — это механизм, позволяющий боту "помнить", на каком этапе диалога находится конкретный пользователь, и сохранять связанные с этим данные.

Без FSM бот реагирует на каждое сообщение изолированно. С FSM вы можете создавать сценарии: опросы, меню, пошаговые формы.

Определение состояний
---------------------

Состояния группируются в классы, наследуемые от `StatesGroup`. Каждое состояние — это экземпляр класса `State`.

.. code-block:: python

    from maxo.fsm import State, StatesGroup

    class Registration(StatesGroup):
        waiting_name = State()
        waiting_age = State()
        waiting_bio = State()

Переходы между состояниями
--------------------------

Чтобы переключить пользователя в другое состояние, используется объект `FSMContext`, который автоматически передается в обработчик, если указать аргумент `state`.

.. code-block:: python

    from maxo.routing.ctx import Ctx
    from maxo.fsm import FSMContext
    from maxo.utils.facades import MessageCreatedFacade
    # Импортируйте вашу группу состояний
    # from states import Registration

    @router.message_created(Command("register"))
    async def start_registration(update, ctx, facade, state: FSMContext):
        await facade.answer_text("Как вас зовут?")
        # Устанавливаем состояние "ожидание имени"
        await state.set_state(Registration.waiting_name)

Фильтрация по состоянию
-----------------------

Чтобы обработчик сработал только в определенном состоянии, используйте `StateFilter`.

.. code-block:: python

    from maxo.fsm import StateFilter

    # Этот хендлер сработает только если пользователь находится в состоянии waiting_name
    @router.message_created(StateFilter(Registration.waiting_name))
    async def process_name(update, ctx, facade, state: FSMContext):
        name = update.message.body.text
        
        # Сохраняем данные в память FSM
        await state.update_data(name=name)
        
        await facade.answer_text(f"Приятно познакомиться, {name}! Сколько вам лет?")
        # Переходим к следующему шагу
        await state.set_state(Registration.waiting_age)

Работа с данными
----------------

`FSMContext` позволяет не только переключать состояния, но и хранить данные, специфичные для текущего пользователя и диалога.

- ``await state.update_data(key=value)`` — добавить или обновить данные.
- ``await state.get_data()`` — получить все сохраненные данные (словарь).
- ``await state.get_value("key")`` — получить конкретное значение.
- ``await state.clear()`` — сбросить состояние и очистить все данные (завершить диалог).

.. code-block:: python

    @router.message_created(StateFilter(Registration.waiting_age))
    async def process_age(update, ctx, facade, state: FSMContext):
        age = update.message.body.text
        
        # Получаем сохраненные ранее данные
        data = await state.get_data()
        name = data.get("name")
        
        await facade.answer_text(f"Анкета:\nИмя: {name}\nВозраст: {age}")
        
        # Завершаем диалог
        await state.clear()

Хранилища
--------------------

Данные FSM должны где-то храниться. **maxo** поддерживает несколько бэкендов.

MemoryStorage
~~~~~~~~~~~~~

Используется по умолчанию, если вы не указали иное при создании `Dispatcher`. Хранит данные в оперативной памяти (RAM).
**Внимание:** При перезапуске бота все состояния сбрасываются. Подходит для разработки.

.. code-block:: python

    from maxo import Dispatcher
    from maxo.fsm.storages.memory import MemoryStorage

    dispatcher = Dispatcher(storage=MemoryStorage())

RedisStorage
~~~~~~~~~~~~

Сохраняет состояния в Redis. Идеально для продакшена: данные переживают перезапуск бота, и можно запускать несколько экземпляров бота параллельно.
Требует установки `redis` (`pip install maxo[redis]`).

.. code-block:: python

    from maxo import Dispatcher
    from maxo.fsm.storages.redis import RedisStorage

    storage = RedisStorage.from_url("redis://localhost:6379/0")
    dispatcher = Dispatcher(storage=storage)
