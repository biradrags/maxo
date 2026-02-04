from maxo.enums.button_type import ButtonType
from maxo.types.button import Button


class CallbackButton(Button):
    """После нажатия на такую кнопку клиент отправляет на сервер полезную нагрузку, которая содержит"""

    type: ButtonType = ButtonType.CALLBACK

    payload: str
