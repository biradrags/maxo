import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from maxo.webhook.security import IPFilter, ip_filter_middleware


@pytest.mark.asyncio
async def test_ip_filter_allows_valid() -> None:
    async def ok_handler(_: web.Request) -> web.Response:
        return web.Response(status=200)

    app = web.Application()
    app.middlewares.append(ip_filter_middleware(IPFilter("127.0.0.1")))
    app.router.add_post("/webhook", ok_handler)

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post(
        "/webhook",
        json={},
        headers={"X-Forwarded-For": "127.0.0.1"},
    ) as resp:
        assert resp.status == 200


@pytest.mark.asyncio
async def test_ip_filter_blocks_invalid() -> None:
    async def ok_handler(_: web.Request) -> web.Response:
        return web.Response(status=200)

    app = web.Application()
    app.middlewares.append(ip_filter_middleware(IPFilter("127.0.0.1")))
    app.router.add_post("/webhook", ok_handler)

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post(
        "/webhook",
        json={},
        headers={"X-Forwarded-For": "1.2.3.4"},
    ) as resp:
        assert resp.status == 401
