from dataclasses import dataclass, field
from motor.core import AgnosticClient
from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.converters import convert_chat_entity_to_document


@dataclass
class MongoDBChatRepository(BaseChatRepository):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    # _saved_chats: list[Chat] = field(
    #     default_factory=list,
    #     kw_only=True
    # )

    def _get_chat_collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def check_chat_exists_by_title(self, title) -> bool:
        """
        делаем запрос в монг  проверяем лежит ли  нас чат уже с таким тайтлом
        """
        collection = self._get_chat_collection()
        print('----s---',collection.find_one(
            filter={
                'title': title
            }
        ))
        return bool(await collection.find_one(
            filter={
                'title': title
            }
        ))


    async def add_chat(self, chat: Chat) -> None:
        """
        так же мы должны уметь добавлять новый чат в нашу коллекцию
        """
        collection = self._get_chat_collection()

        await collection.insert_one(
            # конвертируем наш чат в json.. т.е. в то как он будет помещен в бд
            convert_chat_entity_to_document(chat)
        )
        # self._saved_chats.append(chat)


