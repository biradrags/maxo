from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Path
from maxo.types.video_attachment_details import VideoAttachmentDetails


class GetVideoAttachmentDetails(MaxoMethod[VideoAttachmentDetails]):
    """Получить информацио о видео."""

    __url__ = "videos/{video_token}"
    __method__ = "get"

    video_token: Path[str]
