from fastapi import APIRouter, Request

from app.core.config import settings
from app.services.proxy_service import forward_request

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def proxy_auth(
    path: str,
    request: Request,
):
    return await forward_request(
        request=request,
        target_base_url=settings.IDENTITY_SERVICE_URL,
        path=f"/auth/{path}",
    )