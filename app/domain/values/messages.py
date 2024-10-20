from dataclasses import dataclass

from domain.exceptions.messages import TitleToolLongException, EmptyTextxException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextxException(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextxException(self.value)
        if len(self.value) > 255:
            raise TitleToolLongException(self.value)

    def as_generic_type(self):
        return str(self.value)
