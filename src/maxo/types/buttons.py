from maxo.types.button import Button
from maxo.types.callback_button import CallbackButton
from maxo.types.chat_button import ChatButton
from maxo.types.link_button import LinkButton
from maxo.types.message_button import MessageButton
from maxo.types.open_app_button import OpenAppButton
from maxo.types.reply_button import ReplyButton
from maxo.types.request_contact_button import RequestContactButton
from maxo.types.request_geo_location_button import RequestGeoLocationButton
from maxo.types.send_contact_button import SendContactButton
from maxo.types.send_geo_location_button import SendGeoLocationButton
from maxo.types.send_message_button import SendMessageButton

InlineButtons = (
    CallbackButton
    | LinkButton
    | RequestGeoLocationButton
    | RequestContactButton
    | OpenAppButton
    | MessageButton
    | ChatButton
    | Button
)

ReplyButtons = (
    SendMessageButton | SendGeoLocationButton | SendContactButton | ReplyButton
)
