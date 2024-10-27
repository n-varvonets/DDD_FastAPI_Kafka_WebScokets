from punq import Container
from pytest import fixture
from infra.repositories.messages import BaseChatRepository
from logic.mediator import Mediator
from tests.fixtures import init_dummy_container


@fixture(scope='function')  # хз чего такой скоуп
def container() -> Container:
    return init_dummy_container()


@fixture(scope='function')
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture(scope='function')
def chat_repository(container: Container) -> BaseChatRepository:
    """
    #  для теста получим MemoryChatRepository,
    # т.к. регистрируем в конфитесте, а chat_repository прокидывается в сами тесты
    test_create_chat_command_success
    test_create_chat_command_title_already_exists
    уже используют переданные парамтры-функции из конфитеста
    """
    return container.resolve(BaseChatRepository)

#################################################
### old not combined into one container logic ###
#################################################

# @fixture(scope='function')  # Область видимости изменена на 'function', чтобы создать новый экземпляр для каждого теста
# def chat_repository() -> MemoryChatRepository:
#     """
#     Создание фикстуры репозитория чатов для каждого теста.
#     Использование области видимости 'function' означает, что каждый тест будет иметь свой собственный экземпляр
#     chat_repository. Это необходимо для предотвращения конфликта данных между тестами.
#     """
#     return MemoryChatRepository()
#
#
# @fixture(scope='function')  # Область видимости изменена на 'function', чтобы создать новый экземпляр для каждого теста..  AssertionError: assert 2 == 1
# def mediator(chat_repository: BaseChatRepository) -> Mediator:
#     """
#     Создание фикстуры медиатора для каждого теста.
#     init_mediator получает mediator и chat_repository в качестве аргументов и регистрирует обработчики команд
#     для медиатора. Таким образом, медиатор знает, как взаимодействовать с chat_repository для выполнения команд,
#     связанных с чатами (например, создание чата).
#
#     Область видимости 'function' гарантирует, что каждый тест получает свой собственный экземпляр Mediator,
#     и, как результат, свой собственный экземпляр chat_repository.
#
#     pytest автоматически передаёт результат выполнения фикстуры chat_repository в аргумент chat_repository.
#     Это называется внедрением зависимостей (dependency injection).
#     """
#     mediator = Mediator(mediator=mediator, chat_repository=chat_repository)
#     return mediator
