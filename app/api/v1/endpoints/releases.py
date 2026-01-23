from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ....services.release_service import release_service
from ....models.release_models import LamiNodeRelease
from ....core.logging_config import logger

router = APIRouter()

@router.get("/latest", response_model=LamiNodeRelease)
async def get_latest_release():
    """
    Get the latest release information.
    """
    return release_service.get_latest_release()

@router.get("/check-update", response_model=Optional[LamiNodeRelease])
async def check_update(current_version: str):
    """
    Check if a newer version is available.
    """
    logger.info(f"Checking updates for version: {current_version}")
    return release_service.check_for_update(current_version)

@router.get("/all", response_model=List[LamiNodeRelease])
async def list_all_releases():
    """
    List all releases.
    """
    return release_service.list_releases()
