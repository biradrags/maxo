from maxo.enums.chat_admin_permission import ChatAdminPermission
from maxo.types.base import MaxoType


class ChatAdmin(MaxoType):
    alias: str
    permissions: list[ChatAdminPermission]
    user_id: int
