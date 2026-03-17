from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Dict, List

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.services.maps_services import maps_service
from app.services.preference_service import PreferenceService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/", response_model=List[Dict[str, Any]])
def get_recommendations(
    latitude: float = Query(..., description="Latitude of the user", ge=-90, le=90),
    longitude: float = Query(..., description="Longitude of the user", ge=-180, le=180),
    radius: int = Query(1500, description="Search radius in meters", ge=100, le=50000),
    limit: int = Query(10, description="Maximum number of results to return", ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Return personalised place recommendations for the authenticated user.

    The engine works as follows:
    1. Fetch the user's saved preferences (category / subcategory pairs).
    2. For each preference, query Google Maps for nearby places matching
       the preference category as a place type.
    3. Deduplicate results by place_id.
    4. Sort by rating (descending), boosting places whose types overlap
       with the user's preferred categories.
    5. Return the top `limit` results.

    If the user has no preferences, generic nearby places are returned
    without type filtering.

    - **latitude**: GPS latitude (-90 to 90)
    - **longitude**: GPS longitude (-180 to 180)
    - **radius**: Search radius in meters (default 1500 m)
    - **limit**: Maximum number of results (default 10, max 50)
    """
    preferences = PreferenceService.get_user_preferences(db, current_user.id)

    # Collect unique categories from user preferences
    preferred_categories = {pref.category.lower() for pref in preferences}

    seen_place_ids: set = set()
    all_places: List[Dict[str, Any]] = []

    if preferences:
        # Query Maps for each distinct category the user prefers
        queried_categories: set = set()
        for pref in preferences:
            category = pref.category.lower()
            if category in queried_categories:
                continue
            queried_categories.add(category)

            places = maps_service.get_nearby_places(
                latitude=latitude,
                longitude=longitude,
                radius=radius,
                place_type=category
            )
            for place in places:
                place_id = place.get("place_id")
                if place_id and place_id not in seen_place_ids:
                    seen_place_ids.add(place_id)
                    all_places.append(place)
    else:
        # No preferences -- return generic nearby places
        places = maps_service.get_nearby_places(
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
        for place in places:
            place_id = place.get("place_id")
            if place_id and place_id not in seen_place_ids:
                seen_place_ids.add(place_id)
                all_places.append(place)

    def _sort_key(place: Dict[str, Any]):
        """
        Primary sort: whether the place types overlap with user preferences
        (preferred = True sorts before False).
        Secondary sort: rating descending (missing rating treated as 0).
        """
        place_types = {t.lower() for t in place.get("types", [])}
        matches_preference = bool(place_types & preferred_categories)
        rating = place.get("rating") or 0
        return (not matches_preference, -rating)

    all_places.sort(key=_sort_key)

    return all_places[:limit]
