from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from yarl import URL

from maxo.webhook.adapters.base import BoundRequest

if TYPE_CHECKING:
    from maxo.bot.bot import Bot


class BaseRouting(ABC):
    def __init__(self, url: str) -> None:
        self._url = URL(url)
        self.path = self._url.path
        self.url_template = self._url.human_repr()

    @abstractmethod
    def webhook_point(self, bot: Bot) -> str:
        raise NotImplementedError


class TokenRouting(BaseRouting, ABC):
    def __init__(self, url: str, param: str = "bot_token") -> None:
        super().__init__(url=url)
        self.param = param

    @abstractmethod
    def extract_token(self, bound_request: BoundRequest) -> str | None:
        raise NotImplementedError


class BotIdRouting(BaseRouting, ABC):
    def __init__(self, url: str, param: str = "bot_id") -> None:
        super().__init__(url=url)
        self.param = param

    @abstractmethod
    def extract_bot_id(self, bound_request: BoundRequest) -> int | None:
        raise NotImplementedError

    @abstractmethod
    def webhook_point_for_id(self, bot_id: int) -> str:
        raise NotImplementedError

    def webhook_point(self, bot: Bot) -> str:
        return self.webhook_point_for_id(bot.state.info.user_id)
