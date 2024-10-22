from pytest import fixture

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.init import init_mediator
from logic.mediator import Mediator


@fixture(scope='package')
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()


@fixture(scope='package')
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    """
    init_mediator получает mediator и chat_repository в качестве аргументов и регистрирует обработчики команд
    для медиатора. Таким образом, медиатор знает, как взаимодействовать с chat_repository для выполнения команд,
    связанных с чатами (например, создание чата).

    pytest автоматически передаёт результат выполнения фикстуры chat_repository в аргумент chat_repository.
    Это называется внедрение зависимостей (dependency injection).

    """
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
    return mediator
