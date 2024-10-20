from dataclasses import dataclass

from domain.values.base import BaseValueObject


@dataclass(eq=False)
class ApplicationException(Exception):
    # eq=False - потмоу что ексепшены не сравниваются в практике(за ненадобностью)
    @property
    def message(self):
        return "Application Error occurred"