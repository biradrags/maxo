from maxo import Router
from maxo.routing.filters import CommandStart
from maxo.routing.updates import MessageCreated
from maxo.utils.facades import MessageCreatedFacade

start_router = Router("handlers.start")


@start_router.message_created(CommandStart())
async def start_handler(
    message: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    await facade.answer_text("Привет! Я бот, собранный из нескольких модулей. Напиши что-нибудь — отвечу эхом.")
