from datetime import datetime
from typing import ClassVar

from maxo.enums import UpdateType
from maxo.types.base import MaxoType


class BaseUpdate(MaxoType):
    pass


class MaxUpdate(BaseUpdate):
    type: ClassVar[UpdateType]
    timestamp: datetime
