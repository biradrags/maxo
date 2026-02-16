from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType


class BotCommand(MaxoType):
    """
    до 32 элементов
    Команды, поддерживаемые ботом

    Args:
        description: Описание команды
        name: Название команды
    """

    name: str
    """Название команды"""

    description: Omittable[str | None] = Omitted()
    """Описание команды"""

    @property
    def unsafe_description(self) -> str:
        if is_defined(self.description):
            return self.description

        raise AttributeIsEmptyError(
            obj=self,
            attr="description",
        )
