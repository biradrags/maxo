from maxo.enums.markup_element_type import MarkupElementType
from maxo.types.markup_element import MarkupElement


class EmphasizedMarkup(MarkupElement):
    """Представляет *курсив*"""

    type: MarkupElementType = MarkupElementType.EMPHASIZED
