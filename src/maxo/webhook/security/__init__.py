from __future__ import annotations

import ipaddress
from typing import TYPE_CHECKING, Any

from aiohttp import web
from aiohttp.web_middlewares import middleware

from maxo import loggers
from maxo.webhook.security.checks import (
    IPCheck,
    Security,
    SecurityCheck,
    StaticSecretToken,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiohttp.typedefs import Handler


class IPFilter:
    def __init__(
        self,
        *allowed: str
        | ipaddress.IPv4Network
        | ipaddress.IPv6Network
        | ipaddress.IPv4Address
        | ipaddress.IPv6Address,
    ) -> None:
        self._allowed_networks: list[
            ipaddress.IPv4Network | ipaddress.IPv6Network
        ] = []
        self._allowed_addresses: set[
            ipaddress.IPv4Address | ipaddress.IPv6Address
        ] = set()
        for entry in allowed:
            if isinstance(entry, str):
                if "/" in entry:
                    network = ipaddress.ip_network(entry, strict=False)
                    self._allowed_networks.append(network)
                else:
                    self._allowed_addresses.add(ipaddress.ip_address(entry))
            elif isinstance(
                entry, (ipaddress.IPv4Network, ipaddress.IPv6Network),
            ):
                self._allowed_networks.append(entry)
            else:
                self._allowed_addresses.add(entry)

    def __contains__(self, ip: str) -> bool:
        addr = ipaddress.ip_address(ip)
        if addr in self._allowed_addresses:
            return True
        return any(addr in net for net in self._allowed_networks)


def check_ip(ip_filter: IPFilter, request: web.Request) -> tuple[str, bool]:
    if forwarded_for := request.headers.get("X-Forwarded-For", ""):
        forwarded_for, *_ = forwarded_for.split(",", maxsplit=1)
        forwarded_for = forwarded_for.strip()
        return forwarded_for, forwarded_for in ip_filter
    if (
        request.transport is not None
        and (peer_name := request.transport.get_extra_info("peername"))
    ):
        host, _ = peer_name
        return host, host in ip_filter
    return "", False


def ip_filter_middleware(
    ip_filter: IPFilter,
) -> Callable[[web.Request, Handler], Awaitable[Any]]:
    @middleware
    async def _ip_filter_middleware(
        request: web.Request, handler: Handler,
    ) -> Any:
        ip_address, accept = check_ip(ip_filter=ip_filter, request=request)
        if not accept:
            loggers.webhook.warning(
                "Blocking request from unauthorized IP: %s", ip_address,
            )
            raise web.HTTPUnauthorized
        return await handler(request)

    return _ip_filter_middleware


__all__ = (
    "IPCheck",
    "IPFilter",
    "Security",
    "SecurityCheck",
    "StaticSecretToken",
    "check_ip",
    "ip_filter_middleware",
)
