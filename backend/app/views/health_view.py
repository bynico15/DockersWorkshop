from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]
    environment: str
    version: str


class HeartbeatResponse(BaseModel):
    status: Literal["alive"]
