from abc import ABC
from dataclasses import dataclass, field
from motor.core import AgnosticClient
from domain.entities.messages import Chat, Message
from domain.values.messages import Title
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.converters import convert_chat_entity_to_document, convert_chat_document_to_entity, \
    convert_message_document_to_entity, convert_message_entity_to_document


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatsRepository(BaseChatsRepository, BaseMongoDBRepository):

    async def check_chat_exists_by_title(self, title: str) -> bool:
        """
        делаем запрос в монг  проверяем лежит ли  нас чат уже с таким тайтлом
        """
        return bool(await self._collection.find_one(
            filter={
                'title': title
            }
        ))

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        """
        та же самая проверка, только другое поле
        """
        # 1. get chart document from mongoDB
        chat_document = await self._collection.find_one(
            filter={
                'oid': oid
            }
        )
        if not chat_document:
            return None

        # 2. need to convert document into entity
        return convert_chat_document_to_entity(chat_document)

    async def add_chat(self, chat: Chat) -> None:
        """
        так же мы должны уметь добавлять новый чат в нашу коллекцию
        """
        await self._collection.insert_one(
            # конвертируем наш чат в json.. т.е. в то как он будет помещен в бд
            convert_chat_entity_to_document(chat)
        )
        # self._saved_chats.append(chat)


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, chat_oid: str,  message: Message) -> None:
        # добавляем новый документ в массив внутри другого документа в колекции монгодб
        await self._collection.update_one(
            filter={"oid": chat_oid},
            update={
                "$push": {
                    "messages": convert_message_entity_to_document(message),
                }
            }
        )
