from maxo.omit import Omittable, Omitted
from maxo.types.base import MaxoType


class ContactAttachmentRequestPayload(MaxoType):
    name: str | None = None

    contact_id: Omittable[int | None] = Omitted()
    vcf_info: Omittable[str | None] = Omitted()
    vcf_phone: Omittable[str | None] = Omitted()
