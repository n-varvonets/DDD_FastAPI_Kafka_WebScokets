from functools import lru_cache

from punq import Container  # Импорт контейнера для управления зависимостями

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator


def init_mediator(container: Container, mediator: Mediator):
    """
    Инициализация медиатора с использованием контейнера для управления зависимостями.
    Контейнер используется для разрешения зависимости CreateChatCommandHandler, что упрощает процесс создания
    экземпляров и делает код более гибким и тестируемым.

    resolve позволяет контейнеру автоматически создать экземпляр CreateChatCommandHandler, учитывая все его зависимости.

    Разрешение (container.resolve()) — это процесс, когда контейнер предоставляет экземпляр зарегистрированной зависимости.
    Таким образом, когда медиатору нужен обработчик (CreateChatCommandHandler), он просто обращается к контейнеру,
    и контейнер создает и возвращает нужный объект.
    """
    # mediator.register_command(
    #     CreateChatCommand,
    #     [CreateChatCommandHandler(chat_repository=chat_repository)],
    # )
    # Регистрация команды 'CreateChatCommand' с обработчиком, который контейнер автоматически создает и передает
    mediator.register_command(
        CreateChatCommand,
        [container.resolve(CreateChatCommandHandler)],  # Разрешение зависимости через контейнер
    )


# def init_container(container: Container): - т.к. контнейр тут  глобально инититься, то прокидываеть его в функцию
# не нада + нужно закешировать, сделав синглтон коннект через lru_cache
@lru_cache(1)
def init_container():
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

    container.register(BaseChatRepository, MemoryChatRepository)
    container.register(CreateChatCommandHandler)




