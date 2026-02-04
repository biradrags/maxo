from maxo.omit import Omittable, Omitted
from maxo.types.user import User


class UserWithPhoto(User):
    """Объект с общей информацией о пользователе или боте, дополнительно содержит URL аватара и описание"""

    avatar_url: Omittable[str] = Omitted()
    description: Omittable[str | None] = Omitted()
    full_avatar_url: Omittable[str] = Omitted()
