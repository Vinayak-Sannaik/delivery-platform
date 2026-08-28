from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.ai.agent import AIAgent
from app.conversations.repository import ConversationRepository


router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
)

agent = AIAgent()
conversation_repository = ConversationRepository()


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    conversation_id = request.conversation_id

    if not conversation_id:
        conversation_id = (
            conversation_repository.create()
        )

    response = await agent.run(
        conversation_id=conversation_id,
        message=request.message,
    )

    return ChatResponse(
        conversation_id=conversation_id,
        message=response,
    )