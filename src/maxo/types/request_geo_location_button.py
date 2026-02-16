from maxo.enums.button_type import ButtonType
from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.button import Button


class RequestGeoLocationButton(Button):
    """
    После нажатия на такую кнопку клиент отправляет новое сообщение с вложением текущего географического положения пользователя

    Args:
        quick: Если *true*, отправляет местоположение без запроса подтверждения пользователя
        type:
    """

    type: ButtonType = ButtonType.REQUEST_GEO_LOCATION

    quick: Omittable[bool] = Omitted()
    """Если *true*, отправляет местоположение без запроса подтверждения пользователя"""

    @property
    def unsafe_quick(self) -> bool:
        if is_defined(self.quick):
            return self.quick

        raise AttributeIsEmptyError(
            obj=self,
            attr="quick",
        )
