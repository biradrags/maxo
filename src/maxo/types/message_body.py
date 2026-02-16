from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.attachments import Attachments
from maxo.types.base import MaxoType
from maxo.types.inline_keyboard_attachment import InlineKeyboardAttachment
from maxo.types.keyboard import Keyboard
from maxo.types.markup_elements import MarkupElements
from maxo.utils.text_decorations import (
    TextDecoration,
    html_decoration,
    markdown_decoration,
)


class MessageBody(MaxoType):
    """
    Схема, представляющая тело сообщения

    Args:
        attachments: Вложения сообщения. Могут быть одним из типов `Attachment`. Смотрите описание схемы
        markup: Разметка текста сообщения. Для подробной информации загляните в раздел [Форматирование](/docs-api#Форматирование%20текста)
        mid: Уникальный ID сообщения
        seq: ID последовательности сообщения в чате
        text: Новый текст сообщения
    """

    mid: str
    """Уникальный ID сообщения"""
    seq: int
    """ID последовательности сообщения в чате"""

    attachments: list[Attachments] | None = None
    """Вложения сообщения. Могут быть одним из типов `Attachment`. Смотрите описание схемы"""
    text: str | None = None
    """Новый текст сообщения"""

    markup: Omittable[list[MarkupElements] | None] = Omitted()
    """Разметка текста сообщения. Для подробной информации загляните в раздел [Форматирование](/docs-api#Форматирование%20текста)"""

    @property
    def id(self) -> str:
        return self.mid

    @property
    def keyboard(self) -> Keyboard | None:
        if not self.attachments:
            return None
        for attachment in self.attachments:
            if isinstance(attachment, InlineKeyboardAttachment):
                return attachment.payload
        return None

    @property
    def reply_markup(self) -> Keyboard | None:
        return self.keyboard

    def _unparse_entities(self, text_decoration: TextDecoration) -> str:
        text = self.text or ""
        entities = self.markup or []
        return text_decoration.unparse(text=text, entities=entities)

    @property
    def html_text(self) -> str:
        return self._unparse_entities(html_decoration)

    @property
    def md_text(self) -> str:
        return self._unparse_entities(markdown_decoration)

    @property
    def unsafe_attachments(self) -> list[Attachments]:
        if is_defined(self.attachments):
            return self.attachments

        raise AttributeIsEmptyError(
            obj=self,
            attr="attachments",
        )

    @property
    def unsafe_markup(self) -> list[MarkupElements]:
        if is_defined(self.markup):
            return self.markup

        raise AttributeIsEmptyError(
            obj=self,
            attr="markup",
        )

    @property
    def unsafe_text(self) -> str:
        if is_defined(self.text):
            return self.text

        raise AttributeIsEmptyError(
            obj=self,
            attr="text",
        )
