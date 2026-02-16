from maxo.enums.update_type import UpdateType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class BotStarted(MaxUpdate):
    """
    Бот получает этот тип обновления, как только пользователь нажал кнопку `Start`

    Args:
        chat_id: ID диалога, где произошло событие
        payload: Дополнительные данные из дип-линков, переданные при запуске бота
        type:
        user: Пользователь, который нажал кнопку 'Start'
        user_locale: Текущий язык пользователя в формате IETF BCP 47
    """

    type = UpdateType.BOT_STARTED

    chat_id: int
    """ID диалога, где произошло событие"""
    user: User
    """Пользователь, который нажал кнопку 'Start'"""

    payload: Omittable[str | None] = Omitted()
    """Дополнительные данные из дип-линков, переданные при запуске бота"""
    user_locale: Omittable[str] = Omitted()
    """Текущий язык пользователя в формате IETF BCP 47"""

    @property
    def unsafe_payload(self) -> str:
        if is_defined(self.payload):
            return self.payload

        raise AttributeIsEmptyError(
            obj=self,
            attr="payload",
        )

    @property
    def unsafe_user_locale(self) -> str:
        if is_defined(self.user_locale):
            return self.user_locale

        raise AttributeIsEmptyError(
            obj=self,
            attr="user_locale",
        )
