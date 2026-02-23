from __future__ import annotations

from typing import Any, cast

from aiohttp import web
from aiohttp.web import Application, Request
from aiohttp.web_response import Response, json_response

from maxo.webhook.adapters.base import BoundRequest, WebAdapter


class AiohttpBoundRequest(BoundRequest[Request]):
    def __init__(self, request: Request) -> None:
        super().__init__(request)

    async def json(self) -> dict[str, Any]:
        return await self.request.json()

    @property
    def client_ip(self) -> str | None:
        if self.request.transport is not None:
            peer = self.request.transport.get_extra_info("peername")
            if peer is not None:
                return cast(str, peer[0])
        return None

    @property
    def headers(self) -> dict[str, str]:
        return dict(self.request.headers)

    @property
    def query_params(self) -> dict[str, str]:
        return dict(self.request.query)

    @property
    def path_params(self) -> dict[str, Any]:
        return dict(self.request.match_info)


class AiohttpWebAdapter(WebAdapter):
    def bind(self, request: Request) -> AiohttpBoundRequest:
        return AiohttpBoundRequest(request)

    def register(
        self,
        app: Application,
        path: str,
        handler: Any,
        on_startup: Any = None,
        on_shutdown: Any = None,
    ) -> None:
        async def endpoint(request: Request) -> Response:
            return await handler(self.bind(request))

        app.router.add_route("POST", path, endpoint)
        if on_startup is not None:
            app.on_startup.append(on_startup)
        if on_shutdown is not None:
            app.on_shutdown.append(on_shutdown)

    def create_json_response(self, status: int, payload: dict[str, Any]) -> Response:
        return json_response(status=status, data=payload)

    def create_text_response(self, status: int, text: str) -> Response:
        return web.Response(status=status, text=text)
