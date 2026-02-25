import json
from collections.abc import Callable
from typing import Any, Never

from adaptix import Chain, P, Retort, dumper
from aiohttp import ClientSession
from unihttp.clients.aiohttp import AiohttpAsyncClient
from unihttp.http import HTTPResponse
from unihttp.markers import QueryMarker
from unihttp.method import BaseMethod
from unihttp.middlewares import AsyncMiddleware
from unihttp.serializers.adaptix import DEFAULT_RETORT, for_marker

from maxo import loggers
from maxo.__meta__ import __version__
from maxo.bot.warming_up import WarmingUpType, warming_up_retort
from maxo.enums.text_format import TextFormat
from maxo.errors import (
    MaxBotApiError,
    MaxBotBadRequestError,
    MaxBotForbiddenError,
    MaxBotMethodNotAllowedError,
    MaxBotNotFoundError,
    MaxBotServiceUnavailableError,
    MaxBotTooManyRequestsError,
    MaxBotUnauthorizedError,
    MaxBotUnknownServerError,
)
from maxo.omit import Omittable
from maxo.serialization import TAG_PROVIDERS, create_response_loader
from maxo.types import Attachments


class MaxApiClient(AiohttpAsyncClient):
    def __init__(
        self,
        token: str,
        warming_up: bool,
        text_format: TextFormat | None = None,
        base_url: str = "https://platform-api.max.ru/",
        middleware: list[AsyncMiddleware] | None = None,
        session: ClientSession | None = None,
        json_dumps: Callable[[Any], str] = json.dumps,
        json_loads: Callable[[str | bytes | bytearray], Any] = json.loads,
    ) -> None:
        self._token = token
        self._warming_up = warming_up
        self._text_format = text_format

        if session is None:
            session = ClientSession()

        if "Authorization" not in session.headers:
            session.headers["Authorization"] = self._token
        if "User-Agent" not in session.headers:
            session.headers["User-Agent"] = f"maxo/{__version__}"

        if middleware is None:
            middleware = []

        request_dumper = self._init_method_dumper()
        response_loader = self._init_response_loader()

        super().__init__(
            base_url=base_url,
            request_dumper=request_dumper,
            response_loader=response_loader,
            middleware=middleware,
            session=session,
            json_dumps=json_dumps,
            json_loads=json_loads,
        )

    def _init_method_dumper(self) -> Retort:
        retort = DEFAULT_RETORT.extend(
            recipe=[
                TAG_PROVIDERS,
                dumper(
                    for_marker(QueryMarker, P[None]),
                    lambda _: "null",
                ),
                dumper(
                    for_marker(QueryMarker, P[bool]),
                    lambda item: int(item),
                ),
                dumper(
                    for_marker(QueryMarker, P[list[str]] | P[list[int]]),
                    lambda seq: ",".join(str(el) for el in seq),
                ),
                dumper(
                    P[TextFormat]
                    | P[TextFormat | None]
                    | P[Omittable[TextFormat]]
                    | P[Omittable[TextFormat | None]],
                    lambda item: item or self._text_format,
                ),
                dumper(
                    P[Attachments],
                    lambda attachment: attachment.to_request(),
                    chain=Chain.FIRST,
                ),
            ],
        )

        if self._warming_up:
            retort = warming_up_retort(retort, warming_up=WarmingUpType.METHOD)

        return retort

    def _init_response_loader(self) -> Retort:
        return create_response_loader(self._warming_up)

    def handle_error(self, response: HTTPResponse, method: BaseMethod[Any]) -> Never:
        # ruff: noqa: PLR2004
        code: str = response.data.get("code") or response.data.get("error_code", "")
        error: str = response.data.get("error") or response.data.get("error_data", "")
        message: str = response.data.get("message", "")

        if response.status_code == 400:
            raise MaxBotBadRequestError(code, error, message)
        if response.status_code == 401:
            raise MaxBotUnauthorizedError(code, error, message)
        if response.status_code == 403:
            raise MaxBotForbiddenError(code, error, message)
        if response.status_code == 404:
            raise MaxBotNotFoundError(code, error, message)
        if response.status_code == 405:
            raise MaxBotMethodNotAllowedError(code, error, message)
        if response.status_code == 429:
            raise MaxBotTooManyRequestsError(code, error, message)
        if response.status_code == 500:
            raise MaxBotUnknownServerError(code, error, message)
        if response.status_code == 503:
            raise MaxBotServiceUnavailableError(code, error, message)
        raise MaxBotApiError(code, error, message)

    def validate_response(self, response: HTTPResponse, method: BaseMethod) -> None:
        if (
            response.ok
            and isinstance(response.data, dict)
            and (
                response.data.get("error_code")
                or response.data.get("success", None) is False
            )
        ):
            loggers.bot_session.warning(
                "Patch the status code from %d to 400 due to an error on the MAX API",
                response.status_code,
            )
            response.status_code = 400
