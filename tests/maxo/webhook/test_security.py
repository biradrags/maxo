from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from maxo.webhook.security import IPCheck, Security, StaticSecretToken


def _bound_request(
    *,
    headers: dict[str, str] | None = None,
    client_ip: str | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        headers=headers or {},
        client_ip=client_ip,
        path_params={},
        query_params={},
    )


@pytest.mark.asyncio
async def test_static_secret_token_valid() -> None:
    sec = StaticSecretToken("abc")
    br = _bound_request(headers={"X-Max-Bot-Api-Secret": "abc"})
    bot = MagicMock()
    assert await sec.verify(bot, br) is True


@pytest.mark.asyncio
async def test_static_secret_token_invalid() -> None:
    sec = StaticSecretToken("abc")
    br = _bound_request(headers={"X-Max-Bot-Api-Secret": "wrong"})
    bot = MagicMock()
    assert await sec.verify(bot, br) is False


@pytest.mark.asyncio
async def test_static_secret_token_missing() -> None:
    sec = StaticSecretToken("abc")
    br = _bound_request(headers={})
    bot = MagicMock()
    assert await sec.verify(bot, br) is False


@pytest.mark.asyncio
async def test_ip_check_allows_address() -> None:
    check = IPCheck("127.0.0.1", include_default=False)
    br = _bound_request(client_ip="127.0.0.1")
    bot = MagicMock()
    assert await check.verify(bot, br) is True


@pytest.mark.asyncio
async def test_ip_check_blocks_address() -> None:
    check = IPCheck("127.0.0.1", include_default=False)
    br = _bound_request(client_ip="1.2.3.4")
    bot = MagicMock()
    assert await check.verify(bot, br) is False


@pytest.mark.asyncio
async def test_security_composes_checks() -> None:
    security = Security(StaticSecretToken("secret"))
    br = _bound_request(headers={"X-Max-Bot-Api-Secret": "secret"})
    bot = MagicMock()
    assert await security.verify(bot, br) is True


@pytest.mark.asyncio
async def test_security_get_secret_token() -> None:
    security = Security(StaticSecretToken("my_secret"))
    bot = MagicMock()
    assert await security.get_secret_token(bot) == "my_secret"
