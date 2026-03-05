from typing import Any

import pytest

from maxo import Bot, Ctx


class MockBotInfo:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id


class MockBotState:
    def __init__(self, user_id: int) -> None:
        self.info = MockBotInfo(user_id)


class MockBot:
    def __init__(self, user_id: int = 1) -> None:
        self.state = MockBotState(user_id)


@pytest.fixture
def bot() -> MockBot:
    return MockBot()


@pytest.fixture
def ctx(update: Any, bot: Bot) -> Ctx:
    ctx = Ctx({"update": update, "bot": bot})
    ctx["ctx"] = ctx
    return ctx
