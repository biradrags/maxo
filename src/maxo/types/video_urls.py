from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class VideoUrls(MaxoType):
    hls: Omittable[str | None] = Omitted()
    mp4_1080: Omittable[str | None] = Omitted()
    mp4_144: Omittable[str | None] = Omitted()
    mp4_240: Omittable[str | None] = Omitted()
    mp4_360: Omittable[str | None] = Omitted()
    mp4_480: Omittable[str | None] = Omitted()
    mp4_720: Omittable[str | None] = Omitted()
