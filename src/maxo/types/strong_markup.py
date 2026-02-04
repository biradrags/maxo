from maxo.enums.markup_element_type import MarkupElementType
from maxo.types.markup_element import MarkupElement


class StrongMarkup(MarkupElement):
    """Представляет **жирный** текст"""

    type: MarkupElementType = MarkupElementType.STRONG
