from fastapi import APIRouter

router = APIRouter(tags=["System-Status"])

from app.services.system_status_service import SystemStatusService
from app.schemas.system_status import SystemStatusResponse, ServiceStatus


system_status_service = SystemStatusService()

@router.get(
    "/system/status",
    response_model=SystemStatusResponse,
)
async def system_status():
    services = await system_status_service.get_status()

    ready = all(
        service["status"] == "healthy"
        for service in services
    )
    
    return SystemStatusResponse(
        ready=ready,
        services=[
            ServiceStatus(**service)
            for service in services
        ],
    )
    
@router.post(
    "/system/warmup",
    response_model=SystemStatusResponse,
)
async def warmup_services():

    services = await system_status_service.warmup()

    ready = all(
        service["status"] == "healthy"
        for service in services
    )

    return SystemStatusResponse(
        ready=ready,
        services=[
            ServiceStatus(**service)
            for service in services
        ],
    )