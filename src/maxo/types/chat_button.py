from maxo.omit import Omittable, Omitted
from maxo.types.button import Button


class ChatButton(Button):
    """
    Кнопка, которая создает новый чат, как только первый пользователь на нее нажмёт.
    BБот будет добавлен в участники чата как администратор.
    MАвтор сообщения станет владельцем чата.
    """

    chat_title: str

    chat_description: Omittable[str | None] = Omitted()
    start_payload: Omittable[str | None] = Omitted()
    uuid: Omittable[int | None] = Omitted()
