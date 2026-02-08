from unihttp.http import HTTPRequest, HTTPResponse
from unihttp.middlewares import AsyncHandler, AsyncMiddleware

from maxo import loggers


# https://t.me/maxo_py/609
# https://t.me/maxo_py/615
class StatusPatchMiddleware(AsyncMiddleware):
    async def handle(
        self,
        request: HTTPRequest,
        next_handler: AsyncHandler,
    ) -> HTTPResponse:
        response = await next_handler(request)
        if (
            response.ok
            and isinstance(response.data, dict)
            and (
                response.data.get("error_code")
                or response.data.get("success", None) is False
            )
        ):
            loggers.bot_session.warning(
                "Patch the status code from %d to 400 due to an error on the MAX API",
                response.status_code,
            )
            response.status_code = 400
        return response
