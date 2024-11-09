from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class ChatWithThatTitleAlreadyExitsException(LogicException):
    title: str
    @property
    def message(self):
        return f"Chat already has such title: {self.title}"


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    chat_oid : str
    @property
    def message(self):
        return f"Chat with {self.chat_oid=} not found"  # синтаксис автоматически вставляет имя переменной вместе с её значением в строк

