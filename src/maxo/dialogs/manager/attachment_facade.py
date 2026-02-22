from maxo import Bot
from maxo.dialogs.api.entities import MediaId
from maxo.dialogs.api.protocols import MediaIdStorageProtocol
from maxo.enums import UploadType
from maxo.utils.facades import AttachmentsFacade
from maxo.utils.upload_media import FSInputFile, InputFile


class DialogAttachmentsFacade(AttachmentsFacade):
    def __init__(
        self,
        bot: Bot,
        media_id_storage: MediaIdStorageProtocol,
    ) -> None:
        super().__init__(bot)
        self.media_id_storage = media_id_storage

    async def upload_media(self, file: InputFile) -> tuple[UploadType, str]:
        type_, token = await super().upload_media(file)

        if isinstance(file, FSInputFile):
            await self.media_id_storage.save_media_id(
                path=file.path,
                url=None,
                type=file.type,
                media_id=MediaId(token=token),
            )

        return type_, token
