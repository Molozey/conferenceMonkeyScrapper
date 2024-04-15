from fastapi import APIRouter
from pydantic import BaseModel
from dataclasses import dataclass
from api_service.logs import create_logger
import pandas as pd
from api_service.database import ENGINE

LOGGER = create_logger(__name__)
router = APIRouter(prefix="/testing", tags=["tests"])


class HealthyResponse(BaseModel):
    message: str
    status_code: int


@router.get("/healthcheck")
async def get_empty() -> HealthyResponse:
    return HealthyResponse(message="OK", status_code=200)
