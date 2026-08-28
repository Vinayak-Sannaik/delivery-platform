from fastapi import HTTPException, status

from app.ai.agent import AIAgent
from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:

    def __init__(self):
        self.agent = AIAgent()

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        if not settings.ai_enabled:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI assistant is currently disabled.",
            )

        response = await self.agent.run(
            request.message,
            request.conversation_id
        )

        return ChatResponse(
            message=response,
            conversation_id=request.conversation_id,
        )