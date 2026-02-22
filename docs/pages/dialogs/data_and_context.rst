=================
Данные и Контекст
=================

Данные, необходимые для рендеринга текста, клавиатур и медиа в окне, берутся из словаря (контекста).

Геттеры (Getters)
=================

Геттер — это функция, возвращающая словарь с данными для шаблонов и форматов. Геттер можно повесить как на всё окно (``Window``), так и на весь диалог (``Dialog``). Словари объединяются.

.. code-block:: python

    async def get_user_data(manager, **kwargs):
        return {
            "name": "Иван",
            "balance": 100
        }

    Window(
        Format("Пользователь {name}, баланс: {balance}"),
        state=SG.main,
        getter=get_user_data
    )

Данные из Middleware
====================

Геттеры поддерживают Dependency Injection (как и обычные хэндлеры ``maxo``). Туда автоматически прокидываются все данные из мидлварей:

.. code-block:: python

    async def get_user_data(user: User, **kwargs):
        # user подставляется из мидлвари
        return {"name": user.full_name}

DialogData и StartData
======================

Помимо геттеров, у ``DialogManager`` есть доступ к состоянию диалога:

* ``manager.start_data``: Данные, переданные при вызове ``manager.start(state, data={...})``. Не мутируют.
* ``manager.dialog_data``: Словарь, в который можно сохранять данные между переходами окон (аналог FSM-хранилища).

Пример использования ``dialog_data``:

.. code-block:: python

    async def on_input(message, widget, manager):
        manager.dialog_data["age"] = message.text
        await manager.next()
