from maxo.errors.base import MaxoError


class MaxBotApiError(MaxoError):
    code: str
    message: str


class MaxBotBadRequestError(MaxBotApiError): ...


class MaxBotForbiddenError(MaxBotApiError): ...


class MaxBotUnauthorizedError(MaxBotApiError): ...


class MaxBotNotFoundError(MaxBotApiError): ...


class MaxBotMethodNotAllowedError(MaxBotApiError): ...


class MaxBotTooManyRequestsError(MaxBotApiError): ...


class MaxBotServiceUnavailableError(MaxBotApiError): ...


class RetvalReturnedServerException(MaxoError): ...
