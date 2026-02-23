from __future__ import annotations

from typing import TYPE_CHECKING

from maxo.webhook.routing.base import BaseRouting

if TYPE_CHECKING:
    from maxo.bot.bot import Bot


class StaticRouting(BaseRouting):
    def webhook_point(self, bot: Bot) -> str:
        return self.url_template
