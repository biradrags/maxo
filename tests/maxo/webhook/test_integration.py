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

SAMPLE_UPDATE = {
    "update_type": "message_created",
    "timestamp": 1700000000000,
    "message": {
        "body": {"mid": "mid.123", "seq": 1, "text": "hello"},
        "recipient": {"chat_id": 456, "chat_type": "dialog"},
        "timestamp": 1700000000000,
    },
}


@pytest.mark.asyncio
async def test_full_request_flow_with_engine() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    bot = MagicMock()
    bot.close = AsyncMock()
    bot.state.started = True
    bot._token = "test"  # noqa: S105
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
    async with client:
        resp = await client.post("/webhook", json=SAMPLE_UPDATE)
        assert resp.status == 200
        dp.feed_max_update.assert_awaited_once()

    await engine.on_shutdown(app)
    assert bot.close.await_count >= 1


@pytest.mark.asyncio
async def test_token_engine_dynamic_bot_then_shutdown_closes_all() -> None:
    dp = Dispatcher()
    dp.feed_max_update = AsyncMock()
    adapter = AiohttpWebAdapter()
    routing = PathRouting(url="https://example.com/webhook/bot/{bot_token}")
    with patch("maxo.bot.bot.Bot") as bot_class:
        mock_bot = MagicMock()
        mock_bot.close = AsyncMock()
        mock_bot.start = AsyncMock()
        mock_bot.state.started = True
        mock_bot._token = "dynamic_tok"  # noqa: S105
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
            resp = await client.post(
                "/webhook/bot/dynamic_tok",
                json=SAMPLE_UPDATE,
            )
            assert resp.status == 200
            dp.feed_max_update.assert_awaited_once()
            assert len(engine._bots) == 1

        await engine.on_shutdown(app)
        mock_bot.close.assert_awaited()
        assert len(engine._bots) == 0
