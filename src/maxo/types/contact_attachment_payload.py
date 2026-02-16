from maxo.errors import AttributeIsEmptyError
from maxo.omit import Omittable, Omitted, is_defined
from maxo.types.base import MaxoType
from maxo.types.user import User


class ContactAttachmentPayload(MaxoType):
    """
    Args:
        max_info: Информация о пользователе
        vcf_info: Информация о пользователе в формате VCF.
    """

    max_info: Omittable[User | None] = Omitted()
    """Информация о пользователе"""
    vcf_info: Omittable[str | None] = Omitted()
    """Информация о пользователе в формате VCF."""

    @property
    def unsafe_max_info(self) -> User:
        if is_defined(self.max_info):
            return self.max_info

        raise AttributeIsEmptyError(
            obj=self,
            attr="max_info",
        )

    @property
    def unsafe_vcf_info(self) -> str:
        if is_defined(self.vcf_info):
            return self.vcf_info

        raise AttributeIsEmptyError(
            obj=self,
            attr="vcf_info",
        )
