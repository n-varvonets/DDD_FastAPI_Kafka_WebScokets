import pytest

from domain.entities.messages import Chat
from infra.repositories.messages import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator

@pytest.mark.asyncio  # Маркировка теста как асинхронного, чтобы pytest мог корректно выполнять его
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,  # Фикстура репозитория чатов, в которую сохраняются данные чатов
    mediator: Mediator,  # Фикстура медиатора, который управляет командами и их обработчиками
):
    # TODO: Закончить блок для генерации случайных текстов (возможно, добавить генерацию случайных названий чатов)

    # raise Exception(mediator.commands_map)
    # defaultdict(<class 'list'>, {<class 'logic.commands.messages.CreateChatCommand'>: [CreateChatCommandHandler(chat_repository=MemoryChatRepository(_saved_chats=[]))]


    # Асинхронный вызов метода медиатора для выполнения команды создания чата.
    # Команда CreateChatCommand содержит параметр title='gigaTitle'.
    # Медиатор возвращает список обработанных результатов, и здесь берется первый элемент.
    chat: Chat = (await mediator.handle_command(CreateChatCommand(title='gigaTitle')))[0]

    # Исключение используется временно для отладки, чтобы посмотреть содержимое списка _saved_chats.
    # Это нужно для проверки, что чат был корректно сохранен в репозитории.
    # raise Exception('ssss', chat_repository._saved_chats)

    # Проверка, что созданный чат действительно существует в репозитории.
    # Метод check_chat_exists_by_title должен подтвердить наличие чата с указанным заголовком.
    assert chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())
