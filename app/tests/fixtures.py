from punq import Container, Scope

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.init import _init_container


def init_dummy_container() -> Container:
    """
    container = Container()
    ...
    вместо повторения содержимого в данный метод из init_container,
    мы его для BaseChatRepository вызываем ПРОДОВСКИЙ(init_container с МонгоДбРеп), НО ПРИ ЭТОМ
    - перегестрируем методы, которые нам нужны(для теста с МемориДбРеп) для данной функции (container.register(1,2))
    """
    container = _init_container()

    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    return container



