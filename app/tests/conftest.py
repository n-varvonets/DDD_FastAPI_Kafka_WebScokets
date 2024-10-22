from pytest import fixture
from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.mediator import Mediator
from logic.init import init_mediator

@fixture(scope='function')  # Область видимости изменена на 'function', чтобы создать новый экземпляр для каждого теста
def chat_repository() -> MemoryChatRepository:
    """
    Создание фикстуры репозитория чатов для каждого теста.
    Использование области видимости 'function' означает, что каждый тест будет иметь свой собственный экземпляр
    chat_repository. Это необходимо для предотвращения конфликта данных между тестами.
    """
    return MemoryChatRepository()

@fixture(scope='function')  # Область видимости изменена на 'function', чтобы создать новый экземпляр для каждого теста..  AssertionError: assert 2 == 1
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    """
    Создание фикстуры медиатора для каждого теста.
    init_mediator получает mediator и chat_repository в качестве аргументов и регистрирует обработчики команд
    для медиатора. Таким образом, медиатор знает, как взаимодействовать с chat_repository для выполнения команд,
    связанных с чатами (например, создание чата).

    Область видимости 'function' гарантирует, что каждый тест получает свой собственный экземпляр Mediator,
    и, как результат, свой собственный экземпляр chat_repository.

    pytest автоматически передаёт результат выполнения фикстуры chat_repository в аргумент chat_repository.
    Это называется внедрением зависимостей (dependency injection).
    """
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
    return mediator
