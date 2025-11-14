import html
from typing import Any

from maxo.dialogs.api.protocols import DialogManager
from maxo.dialogs.widgets.common import WhenCondition

from .base import Text


class _FormatDataStub:
    def __init__(self, name="", data=None):
        self.name = name
        self.data = data or {}

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item]
        if not self.name:
            return _FormatDataStub(item)
        return _FormatDataStub(f"{self.name}[{item}]")

    def __getattr__(self, item):
        return _FormatDataStub(f"{self.name}.{item}")

    def __format__(self, format_spec):
        res = f"{self.name}:{format_spec}" if format_spec else self.name
        return f"{{{res}}}"


class Format(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text = text

    async def _render_text(
        self,
        data: dict,
        manager: DialogManager,
    ) -> str:
        if manager.is_preview():
            return self.text.format_map(_FormatDataStub(data=data))
        return self.text.format_map(data)


class _HtmlSafeDict:
    def __init__(self, data: dict) -> None:
        self._data = data

    def __getitem__(self, key: Any) -> str:
        value = self._data[key]
        if isinstance(value, str):
            value = html.escape(value, quote=False)
        return value


class HtmlSafeFormat(Text):
    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(when=when)
        self.text = text

    async def _render_text(
        self,
        data: dict,
        manager: DialogManager,
    ) -> str:
        if manager.is_preview():
            return self.text.format_map(_FormatDataStub(data=data))

        return self.text.format_map(_HtmlSafeDict(data))
