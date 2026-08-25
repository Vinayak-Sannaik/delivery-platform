from app.ai.llm import LLMClient
from app.ai.prompts import SYSTEM_PROMPT


class AIAgent:

    def __init__(self):
        self.llm = LLMClient()

    async def run(
        self,
        message: str,
    ) -> str:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        return await self.llm.generate(messages)