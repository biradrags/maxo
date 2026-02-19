import logging
import os

from maxo import Bot, Dispatcher
from maxo.errors import MaxoError
from maxo.routing.filters import Command, ExceptionTypeFilter
from maxo.routing.updates import ErrorEvent, MessageCreated
from maxo.utils.facades import MessageCreatedFacade
from maxo.utils.long_polling import LongPolling

logger = logging.getLogger(__name__)


TOKEN = os.environ["TOKEN"]

dp = Dispatcher()


class InvalidAge(MaxoError):
    message: str


class InvalidName(ValueError):
    pass


@dp.error(ExceptionTypeFilter(InvalidAge))
async def handle_invalid_age_exception(
    event: ErrorEvent[InvalidAge, MessageCreated],
    facade: MessageCreatedFacade,
) -> None:
    """
    This handler receives only error events with `InvalidAge` exception type.
    """
    assert isinstance(event.error, InvalidAge)  # noqa: S101
    logger.error("Error caught: %r while processing %r", event.error, event.update)

    # Bot instance is passed to the handler as a keyword argument.
    # We can use `bot.send_message` method to send a message to the user,
    # logging the error.
    text = f"Error caught: {event.error!r}"
    await facade.answer_text(text)


@dp.error()
async def handle_invalid_exceptions(
    event: ErrorEvent[Exception, MessageCreated],
    facade: MessageCreatedFacade,
) -> None:
    """
    This handler receives error events with "Invalid" message in them.
    """
    logger.error(
        "Error `Invalid` caught: %r while processing %r",
        event.error,
        event.update,
    )
    await facade.answer_text(f"An unknown error occurred: {event.error!r}")


@dp.message_created(Command("age"))
async def handle_set_age(message: MessageCreated, facade: MessageCreatedFacade) -> None:
    """
    This handler receives only messages with `/age` command.

    If the user sends a message with `/age` command, but the age is invalid,
    the `InvalidAge` exception will be raised and the `handle_invalid_age_exception`
    handler will be called.
    """
    # To get the command object
    # you can use `command` keyword argument with `CommandObject` type.
    # To get the command arguments you can use `command.args` property.
    age = (
        message.message.body.text.split(" ", 1)[1]
        if message.message.body.text and " " in message.message.body.text
        else None
    )
    if not age:
        msg = "No age provided. Please provide your age as a command argument."
        raise InvalidAge(msg)

    # If the age is invalid, raise an exception.
    if not age.isdigit():
        msg = "Age should be a number"
        raise InvalidAge(msg)

    # If the age is valid, send a message to the user.
    age = int(age)
    await facade.reply_text(text=f"Your age is {age}")


@dp.message_created(Command("name"))
async def handle_set_name(
    message: MessageCreated,
    facade: MessageCreatedFacade,
) -> None:
    """
    This handler receives only messages with `/name` command.
    """
    # To get the command object
    # you can use `command` keyword argument with `CommandObject` type.
    # To get the command arguments you can use `command.args` property.
    name = (
        message.message.body.text.split(" ", 1)[1]
        if message.message.body.text and " " in message.message.body.text
        else None
    )
    if not name:
        msg = "Invalid name. Please provide your name as a command argument."
        raise InvalidName(msg)

    # If the name is valid, send a message to the user.
    await facade.reply_text(text=f"Your name is {name}")


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(token=TOKEN)
    LongPolling(dp).run(bot)


if __name__ == "__main__":
    main()
