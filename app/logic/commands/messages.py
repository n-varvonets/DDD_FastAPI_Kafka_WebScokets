# app.logic.commands.messages

from dataclasses import dataclass

from domain.entities.messages import Chat, Message
from domain.values.messages import Title, Text
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.messages import ChatWithThatTitleAlreadyExitsException, ChatNotFoundException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    # Команды не имееют логики, они нужны для того что б
    # закинуть данные в repository классы  и потом отправить эти данные в обработчик(Кафку)

    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    """
    CommandHandler[CreateChatCommand, Chat] представляет собой типизированный обработчик команд,
    где CommandHandler — это обобщённый класс, который параметризован двумя типами:
        - CreateChatCommand указывает тип команды, которую обрабатывает данный обработчик.
        - Chat указывает тип результата, который возвращает метод handle.
    """
    chats_repository: BaseChatsRepository

    # def handle(self, command: CreateChatCommand) -> Chat:
    #     if self.chat_repository.check_chat_exists_by_title(command.title):
    async def handle(self, command: CreateChatCommand) -> Chat:
        # if await self.chat_repository.check_chat_exists_by_title(command.title):
        if await self.chats_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExitsException(command.title)

        title = Title(value=command.title)

        # chat = Chat(title=title)
        # создадим класс в чате лучше на создание чата И РЕГИСТРАЦИЮ ИВЕНТА(что новый чат был создан)
        new_chat = Chat.create_chat(title=title)

        # TODO: считать ивенты
        # await self.chat_repository.add_chat(new_chat)
        await self.chats_repository.add_chat(new_chat)

        # print("command.title", command.title)

        return new_chat

############################
##### message commands #####
############################


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    chat_oid: str
    text: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Message]):
    message_repository: BaseMessagesRepository
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
        if not chat:
            # если чат по айди н существует, то
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        # 1.1.создаем message как сущность - Сообщение всегда должно быть с текстом (иначе ошибка)
        message = Message(text=Text(value=command.text))
        # 1.2. добвляем к ентити Чата его ендиди Мсдж
        chat.add_message(message=message)

        # 2. и записуем ее в месседж репозиторий (мемори, монго) (чат_айди и сам месседж)
        await self.message_repository.add_message(chat_oid=command.chat_oid, message=message)

        return message