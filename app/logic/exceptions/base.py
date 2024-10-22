from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException):
    # eq=False - потмоу что ексепшены не сравниваются в практике(за ненадобностью)
    @property
    def message(self):
        return "Due event handling an error was occured"