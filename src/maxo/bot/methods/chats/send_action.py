from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Path
from maxo.enums.sender_action import SenderAction
from maxo.types.simple_query_result import SimpleQueryResult


class SendAction(MaxoMethod[SimpleQueryResult]):
    """Отправка действия бота в групповой чат."""

    __url__ = "chats/{chat_id}/actions"
    __method__ = "post"

    chat_id: Path[int]

    action: Body[SenderAction]
