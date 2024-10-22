from abc import ABC
from dataclasses import dataclass, field
from uuid import uuid4, UUID


# Базовый класс для всех событий (BaseEvent)
@dataclass(frozen=True)
class BaseEvent:
    """
    BaseEvent — это абстрактный базовый класс для всех событий.
    Каждое событие должно иметь уникальный идентификатор event_id (UUID).
    """
    event_id: UUID = field(default_factory=uuid4, kw_only=True)


