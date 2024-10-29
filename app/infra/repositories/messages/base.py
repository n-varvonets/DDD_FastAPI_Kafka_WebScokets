from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title) -> bool:
        pass

    @abstractmethod
    async def add_chat(self) -> None:
        pass

