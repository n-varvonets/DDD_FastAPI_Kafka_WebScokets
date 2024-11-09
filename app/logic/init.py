from functools import lru_cache

from punq import Container, Scope  # Импорт контейнера для управления зависимостями

from motor.motor_asyncio import AsyncIOMotorClient
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository

from infra.repositories.messages.mongo import MongoDBChatsRepository, MongoDBMessagesRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler, CreateMessageCommand, \
    CreateMessageCommandHandler
from logic.mediator import Mediator
from settings.config import Config


# def init_container(container: Container): - т.к. контнейр тут  глобально инититься, то прокидываеть его в функцию
# не нада + нужно закешировать, сделав синглтон коннект через lru_cache
@lru_cache(1)
def init_container():
    """
    Разделение функций init_container и _init_container позволяет применять декоратор @lru_cache только к внешней функции.
    Это обеспечивает кэширование результата init_container(), сохраняя возможность вызова _init_container() без кэширования,
    что упрощает тестирование и улучшает читаемость кода.
    :return:  cached Container
    """
    return _init_container()


def _init_container() -> Container:
    """
    Регистрация зависимостей в контейнере.
    Контейнер позволяет связывать абстракции с конкретными реализациями.
    Здесь мы регистрируем BaseChatRepository с реализацией MemoryChatRepository.

    SOLID
    - Классы должны быть открыты для расширения, но закрыты для модификации. Абстрактный класс BaseChatRepository
    определяет интерфейс (набор методов), который любая реализация репозитория должна поддерживать, но не конкретизирует реализацию.
    Благодаря этому подходу, можно добавлять новые реализации репозиториев, такие как DatabaseChatRepository для работы
    с реальной базой данных, без изменения существующих классов.

    -   @lru_cache(1): Эта декоратор-функция от модуля functools применяет кэширование "на уровне вызова" к функции init_container.
        Аргумент 1 говорит Python кэшировать единственный результат вызова функции (с одним состоянием параметров).
        В данном случае это обеспечивает создание контейнера только один раз при первом вызове init_container,
        и далее он будет возвращаться из кэша для последующих вызовов.

    -   Синглтон: В этом случае lru_cache работает как простой способ реализации паттерна Singleton для контейнера.
        Это позволяет получить одну и ту же конфигурацию контейнера при повторных вызовах функции.
    """
    # Регистрация зависимости: при запросе BaseChatRepository будет использоваться MemoryChatRepository
    container = Container()

    #  регитсрация зависимостей от никого уровня к более высокому

    # 0. регистрируем репозиторий (МонгоБД, или мемори)
    # 0.1
    # **Factory**: Хорош для случаев, когда необходима гибкость в создании объектов, например, когда параметры
    # объекта могут изменяться в зависимости от контекста или когда требуется ленивая инициализация объекта.
    # container.register(Config, factory=Config, scope=Scope.singleton)

    # 0.2 **Instance**: Лучше подходит для ситуаций, когда объект должен быть создан один раз с немедленной
    # инициализацией всех его зависимостей и параметров, обеспечивая консистентность и предсказуемость на
    # протяжении всего времени работы приложения.
    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)
    def create_mongo_db_client():
        return AsyncIOMotorClient(
            config.mongodb_connection_uri,
            serverSelectionTimeoutMS=3000,
        )
    container.register(AsyncIOMotorClient, factory=create_mongo_db_client, scope=Scope.singleton)
    client = container.resolve(AsyncIOMotorClient)  # т.к. клиент синглтон, то можно его зарезолвить здесь
    def init_chats_mongodb_repository() -> MongoDBChatsRepository:
        return MongoDBChatsRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongo_db_db_name,
            mongo_db_collection_name=config.mongo_db_collection_name,
        )

    def init_messages_mongodb_repository() -> MongoDBMessagesRepository:
        return MongoDBMessagesRepository(
            mongo_db_client=client,
            mongo_db_db_name=config.mongo_db_db_name,
            mongo_db_collection_name=config.mongo_db_collection_name,
        )
    # container.register(BaseChatRepository, MemoryChatRepository)  # без скоупа реквест в swagger будет выполняться в
    # MemoryChatRepository, т.е. не будет сохранен в бд и каждый реквест будет уникальным(не получим 400)...
    # поэтмоу этот контейнер делаем синглтоном
    # container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    # container.register(BaseChatRepository, MongoDBChatRepository, scope=Scope.singleton)
    container.register(BaseChatsRepository, factory=init_chats_mongodb_repository, scope=Scope.singleton)  # factory -
    # Используется, когда создание экземпляра требует предварительной конфигурации или передачи специфических параметров
    container.register(BaseMessagesRepository, factory=init_messages_mongodb_repository, scope=Scope.singleton)

    # 1. регистрируем команды
    # Регистрация CreateChatCommandHandler так, что его зависимости будут автоматически разрешены контейнером
    container.register(CreateChatCommandHandler)
    # Используем container.resolve(CreateChatCommandHandler) для автоматического создания
    # экземпляра CreateChatCommandHandler с его зависимостями, вместо прямого вызова
    # CreateChatCommandHandler(), чтобы получить гибкость и возможность подмены зависимостей.
    container.register(CreateMessageCommandHandler)


    # 2.регистрируем оьект медиатора
    def init_mediator() -> Mediator:
        """
        Инициализация медиатора с использованием контейнера для управления зависимостями.
        Контейнер используется для разрешения зависимости CreateChatCommandHandler, что упрощает процесс создания
        экземпляров и делает код более гибким и тестируемым.

        resolve позволяет контейнеру автоматически создать экземпляр CreateChatCommandHandler, учитывая все его зависимости.

        Разрешение (container.resolve()) — это процесс, когда контейнер предоставляет экземпляр зарегистрированной зависимости.
        Таким образом, когда медиатору нужен обработчик (CreateChatCommandHandler), он просто обращается к контейнеру,
        и контейнер создает и возвращает нужный объект.
        """
        mediator = Mediator()
        # mediator.register_command(
        #     CreateChatCommand,
        #     [CreateChatCommandHandler(chat_repository=chat_repository)],
        # )
        # Регистрация команды 'CreateChatCommand' с обработчиком, который контейнер автоматически создает и передает
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],  # Разрешение зависимости через контейнер
        )
        mediator.register_command(
            CreateMessageCommand,
            [container.resolve(CreateMessageCommandHandler)],  # Разрешение зависимости через контейнер
        )
        return mediator

    container.register(Mediator, factory=init_mediator)  # указывает factory на саму себя (init_mediator),
    # потому что именно эта функция (а не просто вызов конструктора Mediator) обеспечивает полноценное создание
    # и настройку экземпляра Mediator.

    return container
