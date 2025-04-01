from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.events.messages import NewMessageReceivedEvent
from domain.values.messages import Text, Title
from logic.events.messages import NewChatCreatedEvent


@dataclass
class Message(BaseEntity):
    text: Text


########################################
######### Пример использования #########
########################################
# message_correct_1 = Message(text=Text("Hello world"))  # Так правильно, потому что `oid` инициализируется как именованный аргумент.
# message_wrong = Message("some-uuid", Text("Hello world")) # TypeError: __init__() takes 1 positional argument but 2 were given
# message_correct_2 = Message(text=Text("Hello world"), oid="some-uuid")  # Теперь все корректно.

@dataclass
class Chat(BaseEntity):
    title: Title
    messages: list[Message] = field(
        default_factory=list,
        kw_only=True,
    )
    # при создании нового объекта Chat, если для поля messages не будет передано значение, оно будет инициализировано пустым списком
    # нельзя просто передать default=[], mutable types в аргументах
    # Какие еще значения могут быть?
    # - set[Message]  - сключает дубликаты. Множество можно использовать, если важно, чтобы одно и то же сообщение
    # не появлялось несколько раз, но нужно помнить, что порядок элементов в set не сохраняется.

    # - deque[Message]: -  эффективна для добавления и удаления элементов с обоих концов. Может быть полезна,
    # если требуется часто добавлять и удалять сообщения с начала или конца чата.

    # - list[Message]: Это самый распространенный выбор для хранения последовательности сообщений.
    # - Преимущества списка:
    # - - Сохраняет порядок добавления элементов.
    # - - Позволяет добавлять, удалять или изменять сообщения.
    # - - Обеспечивает быстрый доступ к элементам по индексу.
    # - - Если тебе нужно хранить сообщения в порядке их появления и иметь возможность изменять их, то list — это наилучший выбор.

    # - tuple[Message, ...]: Если нужно, чтобы список сообщений был неизменяемым (immutable).
    # Это означает, что однажды создав объект Chat, ты не сможешь добавлять или удалять сообщения в поле messages.
    # - dict[str, Message]: Можно использовать словарь, если необходимо хранить сообщения с уникальными ключами.
    # Например, каждый ключ может быть уникальным идентификатором сообщения (например, oid), а значение — объектом Message.
    # Это позволяет эффективно организовать доступ к сообщениям по ключу, обеспечивая быструю навигацию.

@dataclass
class Chat(BaseEntity):
    title: Title
    messages: list[Message] = field(
        default_factory=list,
        kw_only=True,
    )
    def add_message(self, message: Message):
        self.messages.append(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                chat_oid=self.oid,
                message_oid=message.oid,
            )
        )  # передаем event обьект (NewMessageReceivedEvent)

    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreatedEvent(
            chat_oid=new_chat.oid,
            chat_title=new_chat.title.as_generic_type(),
        ))  # register_event находится в BaseEntity

        return new_chat






