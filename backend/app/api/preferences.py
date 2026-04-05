from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.preference import PreferenceCreate, PreferenceUpdate, PreferenceResponse
from app.services.preference_service import PreferenceService

router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.get("/", response_model=List[PreferenceResponse])
def list_preferences(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    List all preferences for the authenticated user.

    Returns every category / subcategory pair the user has saved.
    """
    return PreferenceService.get_user_preferences(db, current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=PreferenceResponse, status_code=status.HTTP_201_CREATED)
def create_preference(
    preference_data: PreferenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add a new preference for the authenticated user.

    - **category**: Main category (e.g. restaurantes, museos, parques)
    - **subcategory**: Optional sub-category (e.g. comida italiana, arte moderno)

    Returns 409 if an identical category + subcategory already exists for this user.
    """
    is_duplicate = PreferenceService.check_duplicate(
        db,
        user_id=current_user.id,
        category=preference_data.category,
        subcategory=preference_data.subcategory
    )
    if is_duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una preferencia con esa categoria y subcategoria"
        )

    return PreferenceService.create_preference(db, current_user.id, preference_data)


@router.put("/{preference_id}", response_model=PreferenceResponse)
def update_preference(
    preference_id: int,
    preference_data: PreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing preference owned by the authenticated user.

    Supports partial updates -- only the fields provided will be changed.
    Returns 404 if the preference does not exist or does not belong to the user.
    """
    preference = PreferenceService.get_preference_by_id(db, preference_id, current_user.id)
    if preference is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferencia no encontrada"
        )

    return PreferenceService.update_preference(
        db,
        preference=preference,
        category=preference_data.category,
        subcategory=preference_data.subcategory
    )


@router.delete("/{preference_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_preference(
    preference_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a preference owned by the authenticated user.

    Returns 404 if the preference does not exist or does not belong to the user.
    """
    preference = PreferenceService.get_preference_by_id(db, preference_id, current_user.id)
    if preference is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferencia no encontrada"
        )

    PreferenceService.delete_preference(db, preference)
