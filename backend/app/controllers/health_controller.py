from fastapi import APIRouter

from app.core.config import settings
from app.views.health_view import HealthResponse, HeartbeatResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.environment,
        version=settings.app_version,
    )


@router.get("/heartbeat", response_model=HeartbeatResponse)
async def heartbeat() -> HeartbeatResponse:
    return HeartbeatResponse(status="alive")
