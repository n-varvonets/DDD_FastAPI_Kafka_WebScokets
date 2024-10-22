from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExits(LogicException):
    title: str
    @property
    def message(self):
        return f"Chat already has such title: {self.title}"