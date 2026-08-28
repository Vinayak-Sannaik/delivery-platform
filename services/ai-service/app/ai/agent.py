from app.ai.llm import LLMClient
from app.ai.prompts import SYSTEM_PROMPT
from app.tools.executor import ToolExecutor
from app.tools.menu_search import MENU_SEARCH_TOOL
from app.conversations.repository import ConversationRepository

import logging
import json
logger = logging.getLogger(__name__)

class AIAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.tool_executor = ToolExecutor()
        self.conversations = ConversationRepository()
        
    def _save_history(
        self,
        conversation_id: str,
        messages: list[dict],
    ) -> None:

        # Don't store the system prompt
        history = [
            message
            for message in messages
            if message["role"] != "system"
        ]

        history = history[-20:]

        self.conversations.save_messages(
            conversation_id,
            history,
        )

    async def run(
        self,
        conversation_id: str,
        message: str,
    ) -> str:

        history = self.conversations.get_messages(
            conversation_id
        )

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *history,
            {
                "role": "user",
                "content": message,
            },
        ]

        response = await self.llm.chat(
            messages=messages,
            tools=[MENU_SEARCH_TOOL],
        )

        # No tool call
        if not response.tool_calls:

            messages.append(
                {
                    "role": "assistant",
                    "content": response.content,
                }
            )

            self._save_history(
                conversation_id,
                messages,
            )

            return response.content

        # Assistant tool-call message
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

            result = await self.tool_executor.execute(
                tool_name=tool_call.function.name,
                arguments=tool_call.function.arguments,
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

        # Final LLM response
        final_response = await self.llm.chat(
            messages=messages,
        )

        messages.append(
            {
                "role": "assistant",
                "content": final_response.content,
            }
        )

        self._save_history(
            conversation_id,
            messages,
        )

        return final_response.content