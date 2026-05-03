from datetime import datetime
from pydantic import BaseModel
from app.schemas.user import UserResponse


class InviteResponse(BaseModel):
    """Devuelto al creador del invite."""
    id: int
    token: str
    code: str
    expires_at: datetime
    used_at: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class InvitePreview(BaseModel):
    """Info pública de un invite — útil para mostrar antes de aceptar."""
    code: str
    inviter: UserResponse
    expires_at: datetime
    is_valid: bool   # False si expirado o usado


class FriendResponse(BaseModel):
    """Un amigo en la lista de amigos."""
    user: UserResponse
    friendship_id: int
    friends_since: datetime   # responded_at


class FriendshipResponse(BaseModel):
    """Devuelto al aceptar un invite."""
    id: int
    requester: UserResponse
    addressee: UserResponse
    status: str
    created_at: datetime
    responded_at: datetime | None = None

    class Config:
        from_attributes = True
