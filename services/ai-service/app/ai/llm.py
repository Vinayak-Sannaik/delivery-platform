from groq import AsyncGroq

from app.core.config import settings


class LLMClient:

    def __init__(self):
        self.client = AsyncGroq(
            api_key=settings.groq_api_key,
        )

    async def chat(
        self,
        messages: list,
        tools: list | None = None,
    ):

        response = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            tools=tools,
        )

        return response.choices[0].message