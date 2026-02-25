from __future__ import annotations

from typing import TYPE_CHECKING

from maxo.routing.utils import collect_used_updates

if TYPE_CHECKING:
    from collections.abc import Sequence


class WebhookConfig:
    def __init__(
        self,
        *,
        allowed_updates: Sequence[str] | None = None,
        drop_pending_updates: bool | None = None,
    ) -> None:
        self.allowed_updates = list(allowed_updates) if allowed_updates else None
        self.drop_pending_updates = drop_pending_updates

    def resolve_allowed_updates(self, dispatcher: object) -> list[str]:
        if self.allowed_updates is not None:
            return list(self.allowed_updates)
        used = collect_used_updates(dispatcher)
        return [getattr(u, "value", getattr(u, "name", str(u))) for u in used]
