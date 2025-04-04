from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass(frozen=True)
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str
