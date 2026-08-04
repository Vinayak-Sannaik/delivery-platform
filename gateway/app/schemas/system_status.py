from pydantic import BaseModel


class ServiceStatus(BaseModel):
    name: str
    status: str
    latency_ms: float | None = None


class SystemStatusResponse(BaseModel):
    ready: bool
    services: list[ServiceStatus]