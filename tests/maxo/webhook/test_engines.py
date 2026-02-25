from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from maxo.routing.dispatcher import Dispatcher
from maxo.webhook import (
    AiohttpWebAdapter,
    PathRouting,
    SimpleEngine,
    StaticRouting,
    TokenEngine,
    WebhookConfig,
)
from maxo.webhook.security import Security, StaticSecretToken

SAMPLE_UPDATE = {
    "update_type": "message_created",
    "timestamp": 1700000000000,
    "message": {
        "body": {"mid": "mid.123", "seq": 1, "text": "hello"},
        "recipient": {"chat_id": 456, "chat_type": "dialog"},
        "timestamp": 1700000000000,
    },
}

INVALID_UPDATE = {"update_type": "unknown_event", "timestamp": 1700000000000}


def _make_mock_bot() -> MagicMock:
    bot = MagicMock()
    bot.close = AsyncMock()
    bot.start = AsyncMock()
    bot.state.started = True
    bot._token = "test_token"  # noqa: S105
    return bot


@pytest.mark.asyncio
async def test_simple_engine_returns_200() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url="https://example.com/webhook")
    engine = SimpleEngine(
        dp,
        bot,
        web_adapter=adapter,
        routing=routing,
        webhook_config=WebhookConfig(),
    )
    app = web.Application()
    engine.register(app)

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post("/webhook", json=SAMPLE_UPDATE) as resp:
        assert resp.status == 200


@pytest.mark.asyncio
async def test_simple_engine_invalid_json_returns_400() -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url="https://example.com/webhook")
    engine = SimpleEngine(dp, bot, web_adapter=adapter, routing=routing)
    app = web.Application()
    engine.register(app)

    server = TestServer(app)
    client = TestClient(server)
    async with (
        client,
        client.post(
            "/webhook",
            data='{"broken"',
            headers={"Content-Type": "application/json"},
        ) as resp,
    ):
        assert resp.status == 400


@pytest.mark.asyncio
async def test_simple_engine_invalid_content_type_returns_400() -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url="https://example.com/webhook")
    engine = SimpleEngine(dp, bot, web_adapter=adapter, routing=routing)
    app = web.Application()
    engine.register(app)

    server = TestServer(app)
    client = TestClient(server)
    async with (
        client,
        client.post(
            "/webhook",
            data='{"ok": true}',
            headers={"Content-Type": "text/plain"},
        ) as resp,
    ):
        assert resp.status == 400


@pytest.mark.asyncio
async def test_simple_engine_accepts_json_content_type_with_params() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url="https://example.com/webhook")
    engine = SimpleEngine(
        dp,
        bot,
        web_adapter=adapter,
        routing=routing,
        webhook_config=WebhookConfig(),
    )
    app = web.Application()
    engine.register(app)

    server = TestServer(app)
    client = TestClient(server)
    async with (
        client,
        client.post(
            "/webhook",
            json=SAMPLE_UPDATE,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ) as resp,
    ):
        assert resp.status == 200


@pytest.mark.asyncio
async def test_simple_engine_invalid_update_payload_returns_400() -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url="https://example.com/webhook")
    engine = SimpleEngine(dp, bot, web_adapter=adapter, routing=routing)
    app = web.Application()
    engine.register(app)

    server = TestServer(app)
    client = TestClient(server)
    async with client, client.post("/webhook", json=INVALID_UPDATE) as resp:
        assert resp.status == 400


@pytest.mark.asyncio
async def test_simple_engine_secret_valid() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = _make_mock_bot()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url="https://example.com/webhook")
    security = Security(StaticSecretToken("abc"))
    engine = SimpleEngine(
        dp,
        bot,
        web_adapter=adapter,
        routing=routing,
        security=security,
    )
    app = web.Application()
    engine.register(app)

    server = TestServer(app)
    client = TestClient(server)
    async with (
        client,
        client.post(
            "/webhook",
            json=SAMPLE_UPDATE,
            headers={"X-Max-Bot-Api-Secret": "abc"},
        ) as resp,
    ):
        assert resp.status == 200


@pytest.mark.asyncio
async def test_simple_engine_secret_invalid() -> None:
    dp = Dispatcher()
    bot = _make_mock_bot()
    adapter = AiohttpWebAdapter()
    routing = StaticRouting(url="https://example.com/webhook")
    security = Security(StaticSecretToken("abc"))
    engine = SimpleEngine(
        dp,
        bot,
        web_adapter=adapter,
        routing=routing,
        security=security,
    )
    app = web.Application()
    engine.register(app)

    server = TestServer(app)
    client = TestClient(server)
    async with (
        client,
        client.post(
            "/webhook",
            json=SAMPLE_UPDATE,
            headers={"X-Max-Bot-Api-Secret": "wrong"},
        ) as resp,
    ):
        assert resp.status == 401


def test_path_routing_requires_token_placeholder() -> None:
    with pytest.raises(ValueError, match=r"bot_token"):
        PathRouting(url="https://example.com/webhook")


@pytest.mark.asyncio
async def test_token_engine_resolves_bot_from_path_and_feeds_update() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    adapter = AiohttpWebAdapter()
    routing = PathRouting(url="https://example.com/webhook/bot/{bot_token}")
    with patch("maxo.bot.bot.Bot") as bot_class:
        mock_bot = _make_mock_bot()
        mock_bot._token = "tok1"  # noqa: S105
        bot_class.return_value = mock_bot
        engine = TokenEngine(
            dp,
            web_adapter=adapter,
            routing=routing,
            webhook_config=WebhookConfig(),
        )
        app = web.Application()
        engine.register(app)

        server = TestServer(app)
        client = TestClient(server)
        async with (
            client,
            client.post(
                "/webhook/bot/tok1",
                json=SAMPLE_UPDATE,
            ) as resp,
        ):
            assert resp.status == 200
        bot_class.assert_called_once_with(token="tok1")  # noqa: S106
        dp.feed_max_update.assert_awaited_once()


@pytest.mark.asyncio
async def test_token_engine_caches_bot() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    adapter = AiohttpWebAdapter()
    routing = PathRouting(url="https://example.com/webhook/bot/{bot_token}")
    with patch("maxo.bot.bot.Bot") as bot_class:
        mock_bot = _make_mock_bot()
        mock_bot._token = "cached"  # noqa: S105
        bot_class.return_value = mock_bot
        engine = TokenEngine(
            dp,
            web_adapter=adapter,
            routing=routing,
            webhook_config=WebhookConfig(),
        )
        app = web.Application()
        engine.register(app)

        server = TestServer(app)
        client = TestClient(server)
        async with client:
            await client.post("/webhook/bot/cached", json=SAMPLE_UPDATE)
            await client.post("/webhook/bot/cached", json=SAMPLE_UPDATE)
        assert bot_class.call_count == 1


@pytest.mark.asyncio
async def test_token_engine_security_rejects_invalid_secret() -> None:
    dp = Dispatcher()
    adapter = AiohttpWebAdapter()
    routing = PathRouting(url="https://example.com/webhook/bot/{bot_token}")
    security = Security(StaticSecretToken("secret"))
    with patch("maxo.bot.bot.Bot") as bot_class:
        bot_class.return_value = _make_mock_bot()
        engine = TokenEngine(
            dp,
            web_adapter=adapter,
            routing=routing,
            security=security,
            webhook_config=WebhookConfig(),
        )
        app = web.Application()
        engine.register(app)

        server = TestServer(app)
        client = TestClient(server)
        async with (
            client,
            client.post(
                "/webhook/bot/tok1",
                json=SAMPLE_UPDATE,
                headers={"X-Max-Bot-Api-Secret": "wrong"},
            ) as resp,
        ):
            assert resp.status == 401
