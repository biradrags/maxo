from maxo.enums.button_type import ButtonType
from maxo.omit import Omittable, Omitted
from maxo.types.button import Button


class MessageButton(Button):
    """Кнопка для запуска мини-приложения"""

    type: ButtonType = ButtonType.MESSAGE

    text: Omittable[str] = Omitted()
