from pydantic import BaseModel

from domain.entities.messages import Chat


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    """
    что б использовать внутри ендпоинта create_chat_handler
    а method from_entity, что б в ом же методе при return - ее реализовать...
    а классовый, т.к. из класса будет создавать обьект
    """
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return CreateChatResponseSchema(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
        )


class ErrorSchema(BaseModel):
    error: str