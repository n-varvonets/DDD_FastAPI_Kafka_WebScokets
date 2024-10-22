from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, Any

from domain.events.base import BaseEvent

ET = TypeVar('ET', bound=BaseEvent)  # EventType
ER = TypeVar('ER', bound=Any)  #


# Базовый класс для всех обработчиков событий
@dataclass(frozen=True)
class EventHandler(ABC, Generic[ET, ER]):
    """
    EventHandler — это обобщённый класс, который обрабатывает конкретные события (ET).
    Этот класс принимает событие и определяет, как его обработать.
    """
    @abstractmethod
    def handle(self, event: ET) -> None:
        pass
