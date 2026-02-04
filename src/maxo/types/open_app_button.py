from maxo.enums.button_type import ButtonType
from maxo.omit import Omittable, Omitted
from maxo.types.button import Button


class OpenAppButton(Button):
    """Кнопка для запуска мини-приложения"""

    type: ButtonType = ButtonType.OPEN_APP

    contact_id: Omittable[int] = Omitted()
    payload: Omittable[str] = Omitted()
    web_app: Omittable[str] = Omitted()
