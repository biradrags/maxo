from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

R = TypeVar("R")

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


class BoundRequest(ABC, Generic[R]):
    __slots__ = ("request",)

    def __init__(self, request: R) -> None:
        self.request = request

    @abstractmethod
    async def json(self) -> dict[str, Any]:
        raise NotImplementedError

    @property
    @abstractmethod
    def client_ip(self) -> str | None:
        raise NotImplementedError

    @property
    @abstractmethod
    def headers(self) -> dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def query_params(self) -> dict[str, str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def path_params(self) -> dict[str, Any]:
        raise NotImplementedError


class WebAdapter(ABC):
    @abstractmethod
    def bind(self, request: Any) -> BoundRequest:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        app: Any,
        path: str,
        handler: Callable[[BoundRequest], Awaitable[Any]],
        on_startup: Callable[..., Awaitable[Any]] | None = None,
        on_shutdown: Callable[..., Awaitable[Any]] | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_json_response(self, status: int, payload: dict[str, Any]) -> Any:
        raise NotImplementedError
