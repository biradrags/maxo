from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType


class VideoUrls(MaxoType):
    """
    Args:
        hls: URL трансляции, если доступна
        mp4_1080: URL видео в разрешении 1080p, если доступно
        mp4_144: URL видео в разрешении 144p, если доступно
        mp4_240: URL видео в разрешении 240p, если доступно
        mp4_360: URL видео в разрешении 360p, если доступно
        mp4_480: URL видео в разрешении 480p, если доступно
        mp4_720: URL видео в разрешении 720p, если доступно
    """

    hls: Omittable[str | None] = Omitted()
    """URL трансляции, если доступна"""
    mp4_1080: Omittable[str | None] = Omitted()
    """URL видео в разрешении 1080p, если доступно"""
    mp4_144: Omittable[str | None] = Omitted()
    """URL видео в разрешении 144p, если доступно"""
    mp4_240: Omittable[str | None] = Omitted()
    """URL видео в разрешении 240p, если доступно"""
    mp4_360: Omittable[str | None] = Omitted()
    """URL видео в разрешении 360p, если доступно"""
    mp4_480: Omittable[str | None] = Omitted()
    """URL видео в разрешении 480p, если доступно"""
    mp4_720: Omittable[str | None] = Omitted()
    """URL видео в разрешении 720p, если доступно"""

    @property
    def unsafe_hls(self) -> str:
        if is_defined(self.hls):
            return self.hls

        raise AttributeIsEmptyError(
            obj=self,
            attr="hls",
        )

    @property
    def unsafe_mp4_1080(self) -> str:
        if is_defined(self.mp4_1080):
            return self.mp4_1080

        raise AttributeIsEmptyError(
            obj=self,
            attr="mp4_1080",
        )

    @property
    def unsafe_mp4_144(self) -> str:
        if is_defined(self.mp4_144):
            return self.mp4_144

        raise AttributeIsEmptyError(
            obj=self,
            attr="mp4_144",
        )

    @property
    def unsafe_mp4_240(self) -> str:
        if is_defined(self.mp4_240):
            return self.mp4_240

        raise AttributeIsEmptyError(
            obj=self,
            attr="mp4_240",
        )

    @property
    def unsafe_mp4_360(self) -> str:
        if is_defined(self.mp4_360):
            return self.mp4_360

        raise AttributeIsEmptyError(
            obj=self,
            attr="mp4_360",
        )

    @property
    def unsafe_mp4_480(self) -> str:
        if is_defined(self.mp4_480):
            return self.mp4_480

        raise AttributeIsEmptyError(
            obj=self,
            attr="mp4_480",
        )

    @property
    def unsafe_mp4_720(self) -> str:
        if is_defined(self.mp4_720):
            return self.mp4_720

        raise AttributeIsEmptyError(
            obj=self,
            attr="mp4_720",
        )
