import asyncio
import logging
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

INVALID_UPDATE = {
    "update_type": "unknown_event",
    "timestamp": 1700000000000,
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
async def test_simple_handler_invalid_json_returns_400() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=None)
    app = web.Application()
    handler.register(app, path="/webhook")

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post(
        "/webhook",
        data='{"broken"',
        headers={"Content-Type": "application/json"},
    ) as resp:
        assert resp.status == 400


@pytest.mark.asyncio
async def test_simple_handler_invalid_content_type_returns_400() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=None)
    app = web.Application()
    handler.register(app, path="/webhook")

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post(
        "/webhook",
        data='{"ok": true}',
        headers={"Content-Type": "text/plain"},
    ) as resp:
        assert resp.status == 400


@pytest.mark.asyncio
async def test_simple_handler_invalid_update_payload_returns_400() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=None)
    app = web.Application()
    handler.register(app, path="/webhook")

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post("/webhook", json=INVALID_UPDATE) as resp:
        assert resp.status == 400


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


@pytest.mark.asyncio
async def test_simple_handler_close_waits_for_background_tasks() -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    done_event = asyncio.Event()

    async def background_task() -> None:
        await done_event.wait()

    task = asyncio.create_task(background_task())
    handler._background_feed_update_tasks.add(task)

    close_task = asyncio.create_task(handler.close())
    await asyncio.sleep(0)
    assert not close_task.done()
    bot.close.assert_not_awaited()

    done_event.set()
    await close_task
    bot.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_background_task_exception_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    caplog.set_level(logging.ERROR, logger="maxo.webhook")

    async def failing_task() -> None:
        raise RuntimeError("boom")

    task = asyncio.create_task(failing_task())
    handler._background_feed_update_tasks.add(task)
    task.add_done_callback(handler._background_task_done)

    await handler._wait_background_tasks()

    assert "Webhook background task failed" in caplog.text
