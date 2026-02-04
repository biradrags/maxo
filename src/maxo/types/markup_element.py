from maxo.enums import MarkupElementType
from maxo.types.base import MaxoType


class MarkupElement(MaxoType):
    length: int
    name_: int
    type: MarkupElementType
