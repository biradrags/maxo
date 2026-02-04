from maxo.enums import ButtonType
from maxo.types.base import MaxoType


class Button(MaxoType):
    text: str
    type: ButtonType
