from dataclasses import dataclass
from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class TitleToolLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"Too long msg {self.text[:255]}..."


@dataclass(eq=False)
class EmptyTextxException(ApplicationException):
    text: str

    @property
    def message(self):
        return f"There's no any text"
