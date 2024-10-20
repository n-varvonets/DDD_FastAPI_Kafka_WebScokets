from dataclasses import dataclass, field
from uuid import uuid4

from domain.values.messages import Text


@dataclass
class Message:
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )  # поле может быть установлено только через именованный аргумент.
    #  Это означает, что при инициализации объекта данного класса нельзя передавать значение для этого поля
    #  как позиционный аргумент — оно должно быть передано исключительно через ключевое слово (именованный аргумент).
    text: Text


########################################
######### Пример использования #########
########################################
# message_correct_1 = Message(text=Text("Hello world"))  # Так правильно, потому что `oid` инициализируется как именованный аргумент.
# message_wrong = Message("some-uuid", Text("Hello world")) # TypeError: __init__() takes 1 positional argument but 2 were given
# message_correct_2 = Message(text=Text("Hello world"), oid="some-uuid")  # Теперь все корректно.


