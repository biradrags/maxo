from __future__ import annotations

from typing import Any

from adaptix.load_error import AggregateLoadError, LoadError

from maxo import loggers
from maxo.routing.updates import Updates
from maxo.serialization import create_response_loader
from maxo.types.update_list import UpdateList


class AdaptixUpdateParser:
    def __init__(self) -> None:
        self._retort = create_response_loader()

    def parse(self, data: dict[str, Any]) -> Updates:
        try:
            update_list = self._retort.load({"updates": [data]}, UpdateList)
            return update_list.updates[0]
        except (LoadError, AggregateLoadError):
            loggers.webhook.warning("Invalid webhook update payload")
            raise
