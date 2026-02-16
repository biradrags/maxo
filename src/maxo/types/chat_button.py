from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.button import Button


class ChatButton(Button):
    """
    Кнопка, которая создает новый чат, как только первый пользователь на нее нажмёт.
    BБот будет добавлен в участники чата как администратор.
    MАвтор сообщения станет владельцем чата.

    Args:
        chat_description: Описание чата
        chat_title: Название чата, который будет создан
        start_payload: Стартовая полезная нагрузка будет отправлена боту, как только чат будет создан
        uuid: Уникальный ID кнопки среди всех кнопок чата на клавиатуре.
            Если `uuid` изменён, новый чат будет создан при следующем нажатии.
            Сервер сгенерирует его в момент, когда кнопка будет впервые размещена.
            Используйте его при редактировании сообщения.'
    """

    chat_title: str
    """Название чата, который будет создан"""

    chat_description: Omittable[str | None] = Omitted()
    """Описание чата"""
    start_payload: Omittable[str | None] = Omitted()
    """Стартовая полезная нагрузка будет отправлена боту, как только чат будет создан"""
    uuid: Omittable[int | None] = Omitted()
    """
    Уникальный ID кнопки среди всех кнопок чата на клавиатуре.
    Если `uuid` изменён, новый чат будет создан при следующем нажатии.
    Сервер сгенерирует его в момент, когда кнопка будет впервые размещена.
    Используйте его при редактировании сообщения.'
    """

    @property
    def unsafe_chat_description(self) -> str:
        if is_defined(self.chat_description):
            return self.chat_description

        raise AttributeIsEmptyError(
            obj=self,
            attr="chat_description",
        )

    @property
    def unsafe_start_payload(self) -> str:
        if is_defined(self.start_payload):
            return self.start_payload

        raise AttributeIsEmptyError(
            obj=self,
            attr="start_payload",
        )

    @property
    def unsafe_uuid(self) -> int:
        if is_defined(self.uuid):
            return self.uuid

        raise AttributeIsEmptyError(
            obj=self,
            attr="uuid",
        )
