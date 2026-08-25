from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:

    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:

        if not settings.ai_enabled:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI assistant is currently disabled.",
            )

        # Phase 1 placeholder.
        # LLM orchestration will be added next.

        return ChatResponse(
            message=(
                f"AI received your message: "
                f"{request.message}"
            ),
            conversation_id=request.conversation_id,
        )