from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.redis import redis_client


RATE_LIMIT = 100
WINDOW_SECONDS = 60


async def check_rate_limit(request: Request) -> bool:
    client_ip = request.client.host if request.client else "unknown"

    key = f"rate_limit:{client_ip}"

    current_count = await redis_client.incr(key)

    if current_count == 1:
        await redis_client.expire(
            key,
            WINDOW_SECONDS,
        )

    return current_count <= RATE_LIMIT


async def rate_limit(request: Request):
    allowed = await check_rate_limit(request)

    if not allowed:
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests. Please try again later."
            },
            headers={
                "Retry-After": str(WINDOW_SECONDS),
            },
        )

    return None