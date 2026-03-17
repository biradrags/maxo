from typing import Any, cast

from maxo import Bot
from maxo.webhook.adapters.base_adapter import BoundRequest
from maxo.webhook.routing.base import TokenRouting


class QueryRouting(TokenRouting):
    """
    Routing strategy based on the URL query parameter.

    Extracts the bot token from a query parameter in the URL.
    Example: https://example.com/webhook?token=f9LHodD0 will extract the
    token from the query string.
    """

    def webhook_point(self, bot: Bot) -> str:
        return self.url.update_query({self.param: bot.token}).human_repr()

    def extract_token(self, bound_request: BoundRequest[Any]) -> str | None:
        return cast(str | None, bound_request.query_params.get(self.param))
