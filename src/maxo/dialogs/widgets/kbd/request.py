from collections.abc import Callable

from maxo.dialogs.api.internal import RawKeyboard
from maxo.dialogs.api.protocols import DialogManager
from maxo.dialogs.widgets.text import Text
from maxo.omit import Omittable, Omitted
from maxo.types import (
    RequestContactButton,
    RequestGeoLocationButton,
)

from .base import Keyboard


class RequestContact(Keyboard):
    def __init__(
        self,
        text: Text,
        when: str | Callable | None = None,
    ) -> None:
        super().__init__(when=when)
        self.text = text

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        return [
            [
                RequestContactButton(
                    text=await self.text.render_text(data, manager),
                ),
            ],
        ]


class RequestLocation(Keyboard):
    def __init__(
        self,
        text: Text,
        quick: Omittable[bool] = Omitted(),
        when: str | Callable | None = None,
    ) -> None:
        super().__init__(when=when)
        self.text = text
        self.quick = quick

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        return [
            [
                RequestGeoLocationButton(
                    text=await self.text.render_text(data, manager),
                    quick=self.quick,
                ),
            ],
        ]
