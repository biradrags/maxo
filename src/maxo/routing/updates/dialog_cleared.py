from maxo.enums.update_type import UpdateType
from maxo.routing.updates.base import MaxUpdate
from maxo.types.user import User


class DialogCleared(MaxUpdate):
    """Бот получает этот тип обновления сразу после очистки истории диалога."""

    type = UpdateType.DIALOG_CLEARED

    chat_id: int
    user: User
    user_locale: str
