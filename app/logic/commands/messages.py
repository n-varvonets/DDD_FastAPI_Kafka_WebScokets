from dataclasses import dataclass

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages import BaseChatRepository
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.messages import ChatWithThatTitleAlreadyExitsException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    # Команды не имееют логики, они нужны для того что б
    # закинуть данные в классы  и потом отправить эти данные в обработчик(Кафку)

    title: str

@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository

    # def handle(self, command: CreateChatCommand) -> Chat:
    #     if self.chat_repository.check_chat_exists_by_title(command.title):
    async def handle(self, command: CreateChatCommand) -> Chat:
        # if await self.chat_repository.check_chat_exists_by_title(command.title):
        if self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatWithThatTitleAlreadyExitsException(command.title)

        title = Title(value=command.title)

        # chat = Chat(title=title)
        # создадим класс в чате лучше на создание чата И РЕГИСТРАЦИЮ ИВЕНТА(что новый чат был создан)
        new_chat = Chat.create_chat(title=title)

        # TODO: считать ивенты
        # await self.chat_repository.add_chat(new_chat)
        self.chat_repository.add_chat(new_chat)

        return new_chat


