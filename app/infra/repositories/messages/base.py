from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.messages import Chat, Message


@dataclass
class BaseChatsRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title) -> bool:
        pass

    @abstractmethod
    async def get_chat_by_oid(self, title) -> Chat | None:
        pass

    @abstractmethod
    async def add_chat(self) -> None:
        pass

    # async def add_message(self, chat_oid:str, message:Message):
    #     """
    #     Можно было б сделать так, НО(так делать нельзя в ДДД) !!!!
    #     - мы сдеаем отдельный для сообщений НИЖЕ
    #     --- напишем для него тесты как отедльные сущности
    #     --- и потом сделаем АПИшку, которыа будем постить наши сообщения
    #     """


@dataclass
class BaseMessagesRepository(ABC):

    @abstractmethod
    async def add_message(self, chat_oid: str, message: Message) -> None:
        """
        Имплементацию оставим на классах наследниках...
        Т.е. как как это будет: через МонгоДб или Мемори - намс не интересует
        """
        pass
