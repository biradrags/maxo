from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from maxo.enums import ChatType
from maxo.routing.dispatcher import Dispatcher
from maxo.routing.updates import MessageCreated
from maxo.types import Message, MessageBody, Recipient, User
from maxo.webhook.aiohttp_server import SimpleRequestHandler, TokenBasedRequestHandler
from maxo.webhook.security import IPFilter, ip_filter_middleware

SAMPLE_UPDATE = {
    "update_type": "message_created",
    "timestamp": 1700000000000,
    "message": {
        "body": {"mid": "mid.123", "seq": 1, "text": "hello"},
        "sender": {"user_id": 123, "name": "Test"},
        "recipient": {"chat_id": 456, "chat_type": "dialog"},
        "timestamp": 1700000000000,
    },
}

PARSEABLE_UPDATE = {
    "update_type": "message_created",
    "timestamp": 1700000000000,
    "message": {
        "body": {"mid": "mid.123", "seq": 1, "text": "hello"},
        "recipient": {"chat_id": 456, "chat_type": "dialog"},
        "timestamp": 1700000000000,
    },
}


def _make_mock_bot() -> MagicMock:
    bot = MagicMock()
    bot.close = AsyncMock()
    return bot


def _make_message_created() -> MessageCreated:
    return MessageCreated(
        message=Message(
            body=MessageBody(mid="mid.123", seq=1, text="hello"),
            recipient=Recipient(chat_type=ChatType.DIALOG, chat_id=456),
            timestamp=datetime.fromtimestamp(1700000000, tz=UTC),
            sender=User(
                user_id=123,
                first_name="Test",
                is_bot=False,
                last_activity_time=datetime.fromtimestamp(1700000000, tz=UTC),
            ),
        ),
        timestamp=datetime.fromtimestamp(1700000000, tz=UTC),
    )


def test_parse_update_deserializes_message_created() -> None:
    handler = SimpleRequestHandler(dispatcher=Dispatcher(), bot=_make_mock_bot())
    parsed = handler._parse_update(PARSEABLE_UPDATE)
    assert isinstance(parsed, MessageCreated)
    assert parsed.message.body.text == "hello"


@pytest.mark.asyncio
async def test_simple_handler_returns_200() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=None)
    app = web.Application()
    handler.register(app, path="/webhook")
    handler._parse_update = lambda _data: _make_message_created()

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post("/webhook", json=SAMPLE_UPDATE) as resp:
        assert resp.status == 200


@pytest.mark.asyncio
async def test_simple_handler_secret_valid() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    secret = "abc"  # noqa: S105
    handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=secret,
    )
    app = web.Application()
    handler.register(app, path="/webhook")
    handler._parse_update = lambda _data: _make_message_created()

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post(
        "/webhook",
        json=SAMPLE_UPDATE,
        headers={"X-Max-Bot-Api-Secret": "abc"},
    ) as resp:
        assert resp.status == 200


@pytest.mark.asyncio
async def test_simple_handler_secret_invalid() -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    secret = "abc"  # noqa: S105
    handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=secret,
    )
    app = web.Application()
    handler.register(app, path="/webhook")

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post(
        "/webhook",
        json=SAMPLE_UPDATE,
        headers={"X-Max-Bot-Api-Secret": "wrong"},
    ) as resp:
        assert resp.status == 401


@pytest.mark.asyncio
async def test_simple_handler_secret_missing_when_required() -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    secret = "abc"  # noqa: S105
    handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=secret,
    )
    app = web.Application()
    handler.register(app, path="/webhook")

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post("/webhook", json=SAMPLE_UPDATE) as resp:
        assert resp.status == 401


def test_token_based_handler_rejects_no_token_in_path() -> None:
    dp = Dispatcher()
    handler = TokenBasedRequestHandler(dispatcher=dp)
    app = web.Application()
    with pytest.raises(ValueError, match=r"\{bot_token\}"):
        handler.register(app, path="/webhook")


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
