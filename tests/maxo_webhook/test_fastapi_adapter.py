from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from maxo.webhook.adapters.base_adapter import BoundRequest
from maxo.webhook.adapters.fastapi.adapter import FastApiWebAdapter


@pytest.mark.asyncio
async def test_adapter() -> None:
    engine = MagicMock()
    engine.feed_request = AsyncMock()

    async def handler(request: BoundRequest[Any]) -> None:
        await engine.feed_request(request)

    app = FastAPI()
    adapter = FastApiWebAdapter()
    adapter.register(app, "/webhook", handler)

    client = TestClient(app)
    client.post("/webhook", json={"foo": "bar"})

    engine.feed_request.assert_awaited_once()
    request = engine.feed_request.call_args.args[0]
    assert await request.json() == {"foo": "bar"}
