from maxo.enums.chat_admin_permission import ChatAdminPermission
from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ChatAdmin(MaxoType):
    permissions: list[ChatAdminPermission]
    user_id: int

    alias: Omittable[str] = Omitted()
