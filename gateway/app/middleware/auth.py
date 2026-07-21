# Incoming Request
#         │
#         ▼
# Public route?
#         │
#    Yes ─────────► Next

#    No
#         │
# Has Authorization header?
#         │
#    No ──────────► 401

#         │
# Bearer format?
#         │
#    No ──────────► 401

#         │
# Verify JWT
#         │
# Invalid ───────► 401

#         │
# Valid
#         ▼
# call_next(request)

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jwt import InvalidTokenError

from app.security.jwt import verify_access_token


PUBLIC_PREFIXES = (
    "/docs",
    "/redoc",
    "/openapi.json",
    "/auth",
)

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if any(request.url.path.startswith(path) for path in PUBLIC_PREFIXES):
            return await call_next(request)

        authorization = request.headers.get("Authorization")

        if authorization is None:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing."},
            )

        if not authorization.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization header."},
            )

        token = authorization.removeprefix("Bearer ").strip()

        try:
            payload = verify_access_token(token)
            request.state.user = payload

        except InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Gateway received an invalid or expired token."},
            )
            
        print("Gateway: JWT validated")

        return await call_next(request)