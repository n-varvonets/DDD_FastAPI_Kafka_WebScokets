from collections import defaultdict
from dataclasses import dataclass, field
from typing import  Iterable

from domain.events.base import BaseEvent
from logic.commands.base import CommandHandler, CT, CR, BaseCommand
from logic.events.base import EventHandler, ET, ER
from logic.exceptions.mediator import EventHandlersNotRegisteredException, CommandHandlersNotRegisteredException


@dataclass(eq=False)
class Mediator:
    """
    Медиатор отвечает за связывание событий и команд с их обработчиками.

    - events_map: словарь, где ключом является тип события (ET), а значением список обработчиков событий (EventHandler).
    - commands_map: аналогичный словарь для команд и их обработчиков.
    """

    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]) -> None:
        """
        Регистрирует обработчик события.
        - event: объект события (ET).
        - event_handler: обработчик, связанный с этим событием.
        """
        # Получаем класс события и добавляем обработчик в список для данного типа событий
        self.events_map[event].extend(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]) -> None:
        """
        Регистрирует обработчик команды.
        - command: тип команды (CT).
        - command_handler: обработчик, который должен быть вызван при получении команды.
        """
        # Получаем класс команды и добавляем обработчик в список для данного типа команд
        self.commands_map[command].extend(command_handlers)

    # def handle_event(self, event: BaseEvent) -> Iterable[ER]:
    async def publish_event(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        """
        Собранные в пачке ивенты он публиукет в Кафку

        Обрабатывает событие, находя соответствующий обработчик в events_map.
        - event: объект события (BaseEvent).
        """
        event_type = events.__class__  # Получаем тип события
        handlers = self.events_map.get(event_type)  # Получаем обработчики для данного типа события

        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)  # Исключение, если нет зарегистрированных обработчиков

        result = []
        # Вызываем метод handle у каждого обработчика
        # return [handler.handle(event) for handler in handlers]
        # return [await handler.handle(event) for handler in handlers]
        for event in events:
            result.extend([await handler.handle(event) for handler in handlers])
            # [выражение for элемент in итерируемый_объект]
            # await Позволяет ждать результата асинхронного вызова без блокировки основного потока выполнения
            # для асин метода (async def handle(self, event)) объекта handler

        return result

    # def handle_command(self, command: BaseEvent) -> Iterable[CR]:
    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        """
        Обрабатывает событие, находя соответствующий обработчик в events_map.
        - event: объект события (BaseEvent).
        """
        # raise Exception(command.__class__, self.commands_map)
        #  (<class 'logic.commands.messages.CreateChatCommand'>,
        #  defaultdict(<class 'list'>, {<class 'logic.commands.messages.CreateChatCommand'>: [CreateChatCommandHandler(chat_repository=MemoryChatRepository(_saved_chats=[]))]}))
        command_type = command.__class__  # Получаем тип события
        handlers = self.commands_map.get(command_type)  # Получаем обработчики для данного типа события

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)  # Исключение, если нет зарегистрированных обработчиков

        # Вызываем метод handle у каждого обработчика
        # return [handler.handle(command) for handler in handlers]
        return [await handler.handle(command) for handler in handlers]

