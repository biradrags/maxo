import logging
import os
from typing import Any

from magic_filter import F

from maxo import Bot, Dispatcher
from maxo.fsm import FSMContext, State, StateFilter, StatesGroup
from maxo.integrations.magic_filter import MagicFilter
from maxo.routing.filters import AndFilter, CommandStart
from maxo.routing.updates import MessageCreated
from maxo.types import MessageButton
from maxo.utils.builders import KeyboardBuilder
from maxo.utils.facades import MessageCreatedFacade
from maxo.utils.long_polling import LongPolling

logger = logging.getLogger(__name__)

dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()


@dp.message_created(CommandStart())
async def command_start(
    message: MessageCreated,
    facade: MessageCreatedFacade,
    fsm_context: FSMContext,
) -> None:
    await fsm_context.set_state(Form.name)
    await facade.answer_text("Hi there! What's your name?")


@dp.message_created(MagicFilter(F.text.casefold() == "cancel"))
async def cancel_handler(
    message: MessageCreated,
    facade: MessageCreatedFacade,
    fsm_context: FSMContext,
) -> None:
    current_state = await fsm_context.get_state()
    if current_state is None:
        return

    logger.info("Cancelling state %r", current_state)
    await fsm_context.clear()
    await facade.answer_text("Cancelled.")


@dp.message_created(StateFilter(Form.name))
async def process_name(
    message: MessageCreated,
    facade: MessageCreatedFacade,
    fsm_context: FSMContext,
) -> None:
    await fsm_context.update_data(name=message.message.body.text)
    await fsm_context.set_state(Form.like_bots)
    await facade.answer_text(
        f"Nice to meet you, {message.message.body.text}!\nDid you like to write bots?",
        keyboard=KeyboardBuilder()
        .add(
            MessageButton(text="Yes"),
            MessageButton(text="No"),
        )
        .build(),
    )


@dp.message_created(
    AndFilter(
        StateFilter(Form.like_bots),
        MagicFilter(F.text.casefold() == "no"),
    ),
)
async def process_dont_like_write_bots(
    message: MessageCreated,
    facade: MessageCreatedFacade,
    fsm_context: FSMContext,
) -> None:
    data = await fsm_context.get_data()
    await fsm_context.clear()
    await facade.answer_text("Not bad not terrible.\nSee you soon.")
    await show_summary(facade=facade, data=data, positive=False)


@dp.message_created(
    AndFilter(
        StateFilter(Form.like_bots),
        MagicFilter(F.text.casefold() == "yes"),
    ),
)
async def process_like_write_bots(
    message: MessageCreated,
    facade: MessageCreatedFacade,
    fsm_context: FSMContext,
) -> None:
    await fsm_context.set_state(Form.language)
    await facade.reply_text(
        "Cool! I'm too!\nWhat programming language did you use for it?",
    )


@dp.message_created(StateFilter(Form.like_bots))
async def process_unknown_write_bots(
    message: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    await facade.reply_text("I don't understand you :(")


@dp.message_created(StateFilter(Form.language))
async def process_language(
    message: MessageCreated,
    facade: MessageCreatedFacade,
    fsm_context: FSMContext,
) -> None:
    data = await fsm_context.update_data(language=message.message.body.text)
    await fsm_context.clear()

    if message.message.body.text and message.message.body.text.casefold() == "python":
        await facade.reply_text(
            "Python, you say? That's the language that makes my circuits light up! 😉",
        )

    await show_summary(facade=facade, data=data)


async def show_summary(
    facade: MessageCreatedFacade,
    data: dict[str, Any],
    positive: bool = True,
) -> None:
    name = data["name"]
    language = data.get("language", "<something unexpected>")
    text = f"I'll keep in mind that, {name}, "
    text += (
        f"you like to write bots with {language}."
        if positive
        else "you don't like to write bots, so sad..."
    )
    await facade.answer_text(text=text)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(token=os.environ["TOKEN"])
    LongPolling(dp).run(bot)


if __name__ == "__main__":
    main()
