from infra.repositories.messages import MemoryChatRepository, BaseChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator



def init_mediator(mediator: Mediator, chat_repository: BaseChatRepository):
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository)],
    )

    # raise Exception(mediator.commands_map)
    # defaultdict(<class 'list'>, {<class 'logic.commands.messages.CreateChatCommand'>: [CreateChatCommandHandler(chat_repository=MemoryChatRepository(_saved_chats=[]))]})


