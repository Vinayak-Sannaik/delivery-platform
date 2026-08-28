import json
import uuid

from app.core.redis import redis_client


CONVERSATION_TTL = 60 * 60 * 2  # 2 hours


class ConversationRepository:

    def _key(self, conversation_id: str) -> str:
        return f"ai:conversation:{conversation_id}"

    def create(self) -> str:
        conversation_id = str(uuid.uuid4())

        redis_client.setex(
            self._key(conversation_id),
            CONVERSATION_TTL,
            json.dumps([]),
        )

        return conversation_id
    
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

    def get_messages(
        self,
        conversation_id: str,
    ) -> list[dict]:

        data = redis_client.get(
            self._key(conversation_id)
        )

        if not data:
            return []

        return json.loads(data)

    def save_messages(
        self,
        conversation_id: str,
        messages: list[dict],
    ) -> None:

        redis_client.setex(
            self._key(conversation_id),
            CONVERSATION_TTL,
            json.dumps(messages),
        )