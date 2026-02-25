from __future__ import annotations

from maxo.bot.bot import Bot
from maxo.webhook.adapters.base import BoundRequest
from maxo.webhook.routing.base import TokenRouting


class PathRouting(TokenRouting):
    def __init__(self, url: str, param: str = "bot_token") -> None:
        super().__init__(url=url, param=param)
        if f"{{{self.param}}}" not in self.url_template:
            raise ValueError(
                f"Parameter '{self.param}' not found in URL template. "
                f"Expected placeholder '{{{self.param}}}' in: {self.url_template}",
            )

    def webhook_point(self, bot: Bot) -> str:
        return self.url_template.format_map({self.param: bot._token})

    def extract_token(self, bound_request: BoundRequest) -> str | None:
        return bound_request.path_params.get(self.param)
