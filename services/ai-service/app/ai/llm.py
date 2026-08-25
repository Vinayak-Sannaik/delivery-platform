from groq import AsyncGroq

from app.core.config import settings


class LLMClient:

    def __init__(self):
        self.client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

    async def generate(
        self,
        messages: list[dict],
    ):

        response = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
        )

        return response.choices[0].message.content