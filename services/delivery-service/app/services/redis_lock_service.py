# AssignmentService
#     ↓
# Acquire Redis lock
#     ↓
# ┌─────────────────────┐
# │ lock acquired?      │
# └─────────────────────┘
#     │
#    YES ──→ assign partner
#     │          ↓
#     │      DB commit
#     │          ↓
#     │      release lock
#     │
#    NO ──→ another worker is processing it

# The token prevents this bad situation:

# Worker A gets lock
#       ↓
# lock expires
#       ↓
# Worker B gets same lock
#       ↓
# Worker A finishes
#       ↓
# Worker A deletes B's lock ❌

import uuid

from app.core.redis import redis_client


class RedisLockService:

    def acquire(
        self,
        key: str,
        ttl: int = 10,
    ) -> str | None:
        token = str(uuid.uuid4())

        acquired = redis_client.set(
            key,
            token,
            nx=True,
            ex=ttl,
        )

        if not acquired:
            return None

        return token

    def release(
        self,
        key: str,
        token: str,
    ) -> bool:
        current_token = redis_client.get(key)

        if current_token != token:
            return False

        redis_client.delete(key)

        return True