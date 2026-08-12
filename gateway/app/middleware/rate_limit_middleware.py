from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.redis import redis_client


class RateLimitMiddleware(BaseHTTPMiddleware):

    RATE_LIMIT = 100
    WINDOW_SECONDS = 60

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

        key = f"rate_limit:{client_ip}"

        current_count = await redis_client.incr(key)

        if current_count == 1:
            await redis_client.expire(
                key,
                self.WINDOW_SECONDS,
            )

        if current_count > self.RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later."
                },
                headers={
                    "Retry-After": str(self.WINDOW_SECONDS),
                },
            )

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(
            self.RATE_LIMIT
        )

        response.headers["X-RateLimit-Remaining"] = str(
            max(
                0,
                self.RATE_LIMIT - current_count,
            )
        )

        return response