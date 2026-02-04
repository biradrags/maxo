from enum import StrEnum


class ReplyButtonType(StrEnum):
    """After pressing this type of button client will send a message on behalf of user with given payload"""

    MESSAGE = "message"
    USER_CONTACT = "user_contact"
    USER_GEO_LOCATION = "user_geo_location"
