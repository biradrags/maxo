from typing import Any, TypeAlias, TypeVar

from adaptix import Omitted as AdaptixOmitted
from typing_extensions import TypeIs

Omitted = AdaptixOmitted
Omitted.__bool__ = lambda _: False  # Абсолютно осознанное решение

_OmittedValueT = TypeVar("_OmittedValueT")
Omittable: TypeAlias = _OmittedValueT | Omitted


def is_omitted(value: Any) -> TypeIs[Omitted]:
    return isinstance(value, Omitted)


def is_not_omitted(value: Omittable[_OmittedValueT]) -> TypeIs[_OmittedValueT]:
    return not is_omitted(value)


def is_defined(value: Omittable[_OmittedValueT | None]) -> TypeIs[_OmittedValueT]:
    return not isinstance(value, Omitted) and value is not None


def is_not_defined(value: Omittable[_OmittedValueT | None]) -> TypeIs[Omittable[None]]:
    return not is_defined(value)


__all__ = (
    "Omittable",
    "Omitted",
    "is_defined",
    "is_not_defined",
    "is_not_omitted",
    "is_omitted",
)
