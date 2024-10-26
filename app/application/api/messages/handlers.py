from fastapi.routing import APIRouter

router = APIRouter(
    # prefix="chat/",
    tags=["Chat"],
)


@router.post('/')
async def create_chat_handler():
    return {'success': True}
