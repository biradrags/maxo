
import pytest

from maxo.routing.updates import MessageCreated
from maxo.webhook.parsing import AdaptixUpdateParser

PARSEABLE_UPDATE = {
    "update_type": "message_created",
    "timestamp": 1700000000000,
    "message": {
        "body": {"mid": "mid.123", "seq": 1, "text": "hello"},
        "recipient": {"chat_id": 456, "chat_type": "dialog"},
        "timestamp": 1700000000000,
    },
}


def test_parser_deserializes_message_created() -> None:
    parser = AdaptixUpdateParser()
    parsed = parser.parse(PARSEABLE_UPDATE)
    assert isinstance(parsed, MessageCreated)
    assert parsed.message.body.text == "hello"


def test_parser_invalid_payload_raises() -> None:
    parser = AdaptixUpdateParser()
    with pytest.raises(Exception):
        parser.parse({"update_type": "unknown_event", "timestamp": 1700000000000})
