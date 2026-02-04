from maxo.enums import ChatType
from maxo.types.base import MaxoType


# Самодельный объект
class UpdateContext(MaxoType):
    chat_id: int | None = None
    user_id: int | None = None
    type: ChatType | None = None

    @property
    def chat_type(self) -> ChatType | None:
        return self.type
