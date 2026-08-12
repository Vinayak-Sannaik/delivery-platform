from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.redis import redis_client


RATE_LIMIT = 100
WINDOW_SECONDS = 60


class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )

        key = f"rate_limit:ip:{client_ip}"

        current_count = redis_client.incr(key)

        if current_count == 1:
            redis_client.expire(
                key,
                WINDOW_SECONDS,
            )

        if current_count > RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later."
                },
                headers={
                    "Retry-After": str(WINDOW_SECONDS),
                    "X-RateLimit-Limit": str(RATE_LIMIT),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(
            RATE_LIMIT
        )

        response.headers["X-RateLimit-Remaining"] = str(
            max(0, RATE_LIMIT - current_count)
        )

        return response