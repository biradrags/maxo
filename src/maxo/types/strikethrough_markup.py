from maxo.enums.markup_element_type import MarkupElementType
from maxo.types.markup_element import MarkupElement


class StrikethroughMarkup(MarkupElement):
    """Представляет ~зачекрнутый~ текст"""

    type: MarkupElementType = MarkupElementType.STRIKETHROUGH
