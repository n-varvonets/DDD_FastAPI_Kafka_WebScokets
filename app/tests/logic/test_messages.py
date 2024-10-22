import pytest
from faker import Faker

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatWithThatTitleAlreadyExitsException
from logic.mediator import Mediator


@pytest.mark.asyncio  # Маркировка теста как асинхронного, чтобы pytest мог корректно выполнять его
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,  # Фикстура репозитория чатов, в которую сохраняются данные чатов
    mediator: Mediator,  # Фикстура медиатора, который управляет командами и их обработчиками
        faker: Faker
):
    title_text = faker.text()
    chat: Chat = (await mediator.handle_command(CreateChatCommand(title=title_text)))[0]

    # Проверка, что созданный чат действительно существует в репозитории.
    assert chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
        chat_repository: BaseChatRepository,  # Репозиторий для работы с чатами
        mediator: Mediator,  # Обработчик команд
        faker: Faker,  # Фейкер для генерации данных
):
    title_text = faker.text()
    chat = Chat(title=Title(title_text))

    # Добавление чата в репозиторий
    chat_repository.add_chat(chat)

    assert chat in chat_repository._saved_chats

    # Проверка, что исключение возникает при создании чата с тем же названием
    with pytest.raises(ChatWithThatTitleAlreadyExitsException):
        await mediator.handle_command(CreateChatCommand(title=title_text))

    assert len(chat_repository._saved_chats) == 1


