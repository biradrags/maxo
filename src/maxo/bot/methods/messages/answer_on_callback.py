from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Body, Query
from maxo.omit import Omittable, Omitted
from maxo.types.new_message_body import NewMessageBody
from maxo.types.simple_query_result import SimpleQueryResult


class AnswerOnCallback(MaxoMethod[SimpleQueryResult]):
    """Ответ на callback."""

    __url__ = "answers"
    __method__ = "post"

    callback_id: Query[str]

    message: Body[Omittable[NewMessageBody | None]] = Omitted()
    notification: Body[Omittable[str | None]] = Omitted()
