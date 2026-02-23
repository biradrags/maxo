from __future__ import annotations

import ipaddress
import secrets
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from maxo.bot.bot import Bot

from maxo.webhook.adapters.base import BoundRequest


class SecurityCheck(ABC):
    @abstractmethod
    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        raise NotImplementedError


SECRET_HEADER_LOWER = "x-max-bot-api-secret"

DEFAULT_TELEGRAM_NETWORKS: tuple[ipaddress.IPv4Network, ...] = (
    ipaddress.IPv4Network("149.154.160.0/20"),
    ipaddress.IPv4Network("91.108.4.0/22"),
)


def _get_secret_header(headers: dict[str, str]) -> str | None:
    for k, v in headers.items():
        if k.lower() == SECRET_HEADER_LOWER:
            return v
    return None


class StaticSecretToken(SecurityCheck):
    def __init__(self, token: str) -> None:
        self._token = token

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        incoming = _get_secret_header(bound_request.headers)
        if incoming is None:
            return False
        return secrets.compare_digest(incoming, self._token)

    def get_secret(self) -> str:
        return self._token


class IPCheck(SecurityCheck):
    def __init__(
        self,
        *ip_entries: str
        | ipaddress.IPv4Network
        | ipaddress.IPv6Network
        | ipaddress.IPv4Address
        | ipaddress.IPv6Address,
        include_default: bool = True,
    ) -> None:
        self._networks: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = []
        self._addresses: set[ipaddress.IPv4Address | ipaddress.IPv6Address] = set()
        if include_default:
            self._networks.extend(DEFAULT_TELEGRAM_NETWORKS)
        for entry in ip_entries:
            if isinstance(entry, str):
                if "/" in entry:
                    self._networks.append(ipaddress.ip_network(entry, strict=False))
                else:
                    self._addresses.add(ipaddress.ip_address(entry))
            elif isinstance(entry, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
                self._networks.append(entry)
            else:
                self._addresses.add(entry)

    @staticmethod
    def _client_ip(bound_request: BoundRequest) -> str | None:
        forwarded = bound_request.headers.get("x-forwarded-for") or bound_request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",", 1)[0].strip()
        return bound_request.client_ip

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        raw = self._client_ip(bound_request)
        if not raw:
            return False
        try:
            addr = ipaddress.ip_address(raw)
        except ValueError:
            return False
        if addr in self._addresses:
            return True
        return any(addr in net for net in self._networks)


class Security:
    def __init__(
        self,
        *checks: SecurityCheck,
        secret_token: StaticSecretToken | None = None,
    ) -> None:
        self._checks = list(checks)
        if secret_token is not None:
            self._checks.insert(0, secret_token)

    async def verify(self, bot: Bot, bound_request: BoundRequest) -> bool:
        for check in self._checks:
            if not await check.verify(bot, bound_request):
                return False
        return True

    async def get_secret_token(self, bot: Bot) -> str | None:
        for check in self._checks:
            if isinstance(check, StaticSecretToken):
                return check.get_secret()
        return None
