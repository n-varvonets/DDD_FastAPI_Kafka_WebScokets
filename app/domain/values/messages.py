from dataclasses import dataclass

from domain.exceptions.messages import TextToolLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > 255:
            raise TextToolLongException(self.value)
        # return super().validate()

    def as_generic_type(self):
        return str(self.value)