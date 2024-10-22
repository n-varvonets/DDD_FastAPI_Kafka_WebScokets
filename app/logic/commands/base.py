from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

# Команды не имееют логики, они нужны для того что б закинуть данные в классы  и потом отправить эти данные в обработчик(Кафку)

@dataclass(frozen=True)
class BaseCommand(ABC):
    """
    BaseCommand - базовый класс для всех команд.
    Он наследуется от ABC (Abstract Base Class), что позволяет определять
    абстрактные классы, которые нельзя инстанцировать напрямую.
    """

# Тип переменной, представляющей команду. Она ограничена наследниками от BaseCommand.
CT = TypeVar('CT', bound='BaseCommand')  # CommandType.  # Тип команды, который должен наследоваться от BaseCommand.
# Тип переменной, представляющей результат обработки команды. Это может быть любой тип.
CR = TypeVar('CR', bound=Any)  # CommandResult


# Командный обработчик (CommandHandler), который принимает обобщенные типы CT и CR.
# Он также является неизменяемым (frozen=True).
@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    """
    CommandHandler - это обобщенный (Generic) класс, который принимает
    тип команды (CT) и тип результата (CR). Это позволяет создавать
    обработчики команд с различными типами команд и возвращаемых значений.
    """

    @abstractmethod
    # def handle(self, command: CT) -> CR:
    async def handle(self, command: CT) -> CR:
        """
        Абстрактный метод handle, который обязан быть реализован в классах-наследниках.
        Этот метод принимает команду типа CT и возвращает результат типа CR.
        """
        pass



#####################################################################
######### Пример конкретной команды (создание пользователя) #########
#####################################################################

# @dataclass(frozen=True)
# class CreateUserCommand(BaseCommand):
#     username: str
#     email: str
#
# # Пример конкретного обработчика команды
# @dataclass(frozen=True)
# class CreateUserHandler(CommandHandler[CreateUserCommand, int]):
#     """
#     Этот обработчик принимает команду CreateUserCommand и возвращает результат типа int (ID пользователя).
#     """
#     def handle(self, command: CreateUserCommand) -> int:
#         print(f"Creating user: {command.username}, {command.email}")
#         # Здесь обычно идет логика создания пользователя в БД и возврат его ID.
#         return 42  # Пример результата: ID созданного пользователя
#
# # Использование команды и обработчика
# command = CreateUserCommand(username="JohnDoe", email="john@example.com")
# handler = CreateUserHandler()
#
# # Выполняем обработку команды
# result = handler.handle(command)
# print(result)  # Выведет: 42 (ID пользователя)
