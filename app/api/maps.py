from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any
from app.core.deps import get_current_active_user
from app.models.user import User
from app.services.maps_services import maps_service

# Create router with prefix and tag for documentation
router = APIRouter(prefix="/maps", tags=["Maps"])


@router.get("/nearby", response_model=List[Dict[str, Any]])
def get_nearby_places(
    latitude: float = Query(..., description="Latitude of the location", ge=-90, le=90),
    longitude: float = Query(..., description="Longitude of the location", ge=-180, le=180),
    radius: int = Query(1000, description="Search radius in meters", ge=100, le=50000),
    place_type: Optional[str] = Query(None, description="Type of place (restaurant, cafe, museum, park, etc.)"),
    keyword: Optional[str] = Query(None, description="Keyword to filter results"),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get nearby places based on location.

    - **latitude**: GPS latitude (-90 to 90)
    - **longitude**: GPS longitude (-180 to 180)
    - **radius**: Search radius in meters (default: 1000m, max: 50km)
    - **place_type**: Filter by place type (restaurant, cafe, museum, park, etc.)
    - **keyword**: Additional keyword filter (e.g., "italian", "pizza")

    Returns a list of nearby places with their details.
    """
    places = maps_service.get_nearby_places(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
        place_type=place_type,
        keyword=keyword
    )
    return places


@router.get("/place/{place_id}")
def get_place_details(
    place_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed information about a specific place.

    - **place_id**: The Google Maps place ID

    Returns complete details including reviews, opening hours, contact info.
    """
    place = maps_service.get_place_details(place_id)

    if place is None:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place


@router.get("/geocode")
def geocode_address(
    address: str = Query(..., description="Address to convert to coordinates", min_length=3),
    current_user: User = Depends(get_current_active_user)
):
    """
    Convert an address to geographic coordinates.

    - **address**: Full or partial address (e.g., "Gran Via, Madrid")

    Returns the formatted address, coordinates (lat/lng), and place_id.
    """
    result = maps_service.geocode_address(address)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Address not found"
        )

    return result
