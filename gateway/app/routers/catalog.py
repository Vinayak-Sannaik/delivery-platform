from fastapi import APIRouter, Request

from app.core.config import settings
from app.services.proxy_service import forward_request

router = APIRouter(
    prefix="/api",
    tags=["Catalog"],
)


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def proxy_catalog(
    path: str,
    request: Request,
):
    return await forward_request(
        request=request,
        target_base_url=settings.CATALOG_SERVICE_URL,
        path=f"/{path}",
    )