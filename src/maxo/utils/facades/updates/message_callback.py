from maxo.routing.updates.message_callback import MessageCallback
from maxo.types.callback import Callback
from maxo.types.message import Message
from maxo.utils.facades.methods.callback import CallbackMethodsFacade
from maxo.utils.facades.methods.message import MessageMethodsFacade
from maxo.utils.facades.updates.base import BaseUpdateFacade


class MessageCallbackFacade(
    BaseUpdateFacade[MessageCallback], MessageMethodsFacade, CallbackMethodsFacade
):
    @property
    def message(self) -> Message:
        return self._update.unsafe_message

    @property
    def callback(self) -> Callback:
        return self._update.callback
