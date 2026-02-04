from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.chat_member import ChatMember


class GetMembership(MaxoMethod[ChatMember]):
    """Получение информации о членстве бота в групповом чате."""

    __url__ = "chats/{chat_id}/members/me"
    __method__ = "get"

    chat_id: Path[int]
