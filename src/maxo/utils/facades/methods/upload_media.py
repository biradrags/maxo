from unihttp.http import UploadFile

from maxo.bot.bot import Bot
from maxo.errors.api import RetvalReturnedServerException
from maxo.omit import is_defined
from maxo.types import UploadEndpoint
from maxo.utils.upload_media import InputFile


class UploadMediaFacade:
    def __init__(
        self,
        bot: Bot,
        upload_media: InputFile,
    ) -> None:
        self._bot = bot
        self._upload_media = upload_media

    async def upload(self) -> UploadEndpoint:
        upload_media = self._upload_media

        result = await self._bot.get_upload_url(type=upload_media.type)

        try:
            upload_result = await self._bot.upload_media(
                upload_url=result.url,
                file=UploadFile(
                    file=await upload_media.read(),
                    filename=upload_media.file_name,
                ),
            )
        except RetvalReturnedServerException:
            upload_result = None

        if is_defined(result.token):
            return UploadEndpoint(token=result.token)
        if upload_result is not None:
            return upload_result

        raise RuntimeError
