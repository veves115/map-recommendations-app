from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.location import LocationCreate, LocationResponse
from app.services.location_service import LocationService

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def register_location(
    location_data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Record a new location for the authenticated user.

    - **latitude**: GPS latitude (-90 to 90)
    - **longitude**: GPS longitude (-180 to 180)
    - **place_name**: Optional human-readable name for the location
    """
    return LocationService.create_location(db, current_user.id, location_data)


@router.get("/me", response_model=List[LocationResponse])
def get_location_history(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Return the location history for the authenticated user, ordered from
    most recent to oldest.

    - **skip**: Pagination offset (default 0)
    - **limit**: Page size (default 20, max 100)
    """
    return LocationService.get_user_locations(db, current_user.id, skip=skip, limit=limit)


@router.get("/latest", response_model=LocationResponse)
def get_latest_location(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Return the most recent location recorded for the authenticated user.

    Returns 404 if the user has no recorded locations yet.
    """
    location = LocationService.get_latest_location(db, current_user.id)
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron ubicaciones para este usuario"
        )
    return location
