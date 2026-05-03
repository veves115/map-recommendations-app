from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.friendship import (
    InviteResponse,
    InvitePreview,
    FriendResponse,
    FriendshipResponse,
)
from app.services.friendship_service import FriendshipService

router = APIRouter(prefix="/friends", tags=["Friends"])

# -------- Invites --------

@router.post("/invites", response_model=InviteResponse, status_code=status.HTTP_201_CREATED)
def create_invite(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Crear un nuevo link de invitación (token + código corto)"""
    return FriendshipService.create_invite(db, current_user)

@router.get("/invites", response_model=List[InviteResponse])
def list_invites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Listar mis invitaciones activas (no usadas, no caducadas)"""
    return FriendshipService.list_invites(db, current_user)

@router.delete("/invites/{invite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invite(
    invite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Revocar una de mis invitaciones"""
    FriendshipService.delete_invite(db, current_user, invite_id)

@router.get("/invites/lookup/{code}", response_model=InvitePreview)
def lookup_invite(
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Ver info pública de una invitación por código (preview antes de aceptar)"""
    return FriendshipService.lookup_invite_by_code(db, code)

@router.post("/invites/{token}/accept", response_model=FriendshipResponse)
def accept_invite(
    token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Aceptar una invitación (crea la amistad)"""
    return FriendshipService.accept_invite(db, current_user, token)

# -------- Friends --------

@router.get("/", response_model=List[FriendResponse])
def list_friends(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Listar mis amigos aceptados"""
    friendships = FriendshipService.list_friends(db, current_user)
    # Construir respuesta en formato "amigo desde X"
    result = []
    for f in friendships:
        other = f.addressee if f.requester_id == current_user.id else f.requester
        result.append({
            "user": other,
            "friendship_id": f.id,
            "friends_since": f.responded_at,
        })
    return result

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_friend(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Eliminar una amistad"""
    FriendshipService.remove_friend(db, current_user, user_id)
    
@router.post("/invites/code/{code}/accept", response_model=FriendshipResponse)
def accept_invite_by_code(
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Aceptar una invitación usando el código corto (en vez del token)"""
    return FriendshipService.accept_invite_by_code(db, current_user, code)

