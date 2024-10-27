from fastapi import HTTPException, Depends, status
from fastapi.routing import APIRouter
# from application.api.dependencies.containers import container  - используя Depends ушли от глобавльной инициализации
from application.api.messages.schema import CreateChatResponseSchema, CreateChatRequestSchema, ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand
from logic.init import init_container
from logic.mediator import Mediator

router = APIRouter(
    # prefix="chat/",
    tags=["Chat"],
)


@router.post(
    '/',
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint - Creating a new chat. If such chat by title already exists, return 400",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    }
)
async def create_chat_handler(schema: CreateChatRequestSchema, container=Depends(init_container)):
    """
    Создает новый чат
    :param schema: CreateChatRequestSchema - схема что должен принимать (title).
    :param container: Depends(init_container) - используется для инъекции контейнера зависимостей.
                  Depends позволяет автоматически вызвать init_container для получения контейнера
                  при каждом запросе, упрощая управление зависимостями внутри функции.
    :return: Созданный чат или ошибка.
    """
    mediator: Mediator = container.resolve(Mediator)

    try:
        # chat = (await mediator.handle_command(CreateChatCommand(title=schema.title)))[0]
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})
    print(f'chat={chat}')
    return CreateChatResponseSchema.from_entity(chat)
    # return {'success': True}
