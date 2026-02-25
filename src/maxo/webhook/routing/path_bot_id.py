from __future__ import annotations

from maxo.webhook.adapters.base import BoundRequest
from maxo.webhook.routing.base import BotIdRouting


class PathBotIdRouting(BotIdRouting):
    def __init__(self, url: str, param: str = "bot_id") -> None:
        super().__init__(url=url, param=param)
        if f"{{{self.param}}}" not in self.url_template:
            raise ValueError(
                f"Parameter '{self.param}' not found in URL template. "
                f"Expected placeholder '{{{self.param}}}' in: {self.url_template}",
            )

    def webhook_point_for_id(self, bot_id: int) -> str:
        return self.url_template.format_map({self.param: bot_id})

    def extract_bot_id(self, bound_request: BoundRequest) -> int | None:
        raw = bound_request.path_params.get(self.param)
        if raw is None:
            return None
        if isinstance(raw, int):
            return raw
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None
