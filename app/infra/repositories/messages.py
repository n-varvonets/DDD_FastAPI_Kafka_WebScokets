from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from domain.entities.messages import Chat
from domain.values.messages import Title


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    def check_chat_exists_by_title(self, title) -> bool:
        pass

    @abstractmethod
    def add_chat(self) -> None:
        pass


@dataclass
class MemoryChatRepository(ABC):
    # class MemoryChatRepository(BaseChatRepository):
    _saved_chats: list[Chat] = field(
        default_factory=list,
        kw_only=True
    )

    def check_chat_exists_by_title(self, title) -> bool:
        """
        Проверяет, существует ли чат с заданным заголовком в репозитории.

        Аргументы:
        - title: Заголовок, который нужно найти. Ожидается, что это строка.

        Возвращает:
        - True, если чат с таким заголовком существует, иначе False.
        """
        # Приведем переданный заголовок к строке для сравнения с сохраненными объектами Title
        if isinstance(title, Title):  # Если переданный title является объектом Title, берем его значение
            title_value = title.value
        else:
            title_value = title  # Иначе предполагаем, что это уже строка

        # Проверяем, существует ли чат с таким заголовком в сохранённых чатах
        return any(chat.title.value == title_value for chat in self._saved_chats)


    def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

