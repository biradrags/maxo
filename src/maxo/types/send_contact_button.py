from maxo.enums.reply_button_type import ReplyButtonType
from maxo.types.reply_button import ReplyButton


class SendContactButton(ReplyButton):
    """AПосле нажатия на такую кнопку клиент отправляет новое сообщение с вложением текущего контакта пользователя"""

    type: ReplyButtonType = ReplyButtonType.USER_CONTACT
