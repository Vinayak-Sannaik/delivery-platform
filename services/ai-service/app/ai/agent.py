from app.ai.llm import LLMClient
from app.ai.prompts import SYSTEM_PROMPT
from app.tools.executor import ToolExecutor
from app.tools.menu_search import MENU_SEARCH_TOOL
import logging
logger = logging.getLogger(__name__)

class AIAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.tool_executor = ToolExecutor()

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

        response = await self.llm.chat(
            messages=messages,
            tools=[MENU_SEARCH_TOOL],
        )

        # No tool required
        if not response.tool_calls:
            return response.content

        # Convert assistant response to a normal
        # OpenAI-compatible message structure.
        assistant_message = {
            "role": "assistant",
            "content": response.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in response.tool_calls
            ],
        }

        messages.append(assistant_message)

        # Execute tools
        for tool_call in response.tool_calls:

            logger.info(
                "AI tool call: %s arguments=%s",
                tool_call.function.name,
                tool_call.function.arguments,
            )
            result = await self.tool_executor.execute(
                tool_name=tool_call.function.name,
                arguments=tool_call.function.arguments,
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )
            
            logger.info(
                "AI tool completed: %s",
                tool_call.function.name,
            )

        # Ask Groq to produce the final natural-language answer.
        final_response = await self.llm.chat(
            messages=messages,
        )

        return final_response.content