import secrets
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from fastapi import HTTPException, status

from app.models.user import User
from app.models.friendship import Friendship, FriendshipStatus
from app.models.friend_invite import FriendInvite


INVITE_EXPIRY_DAYS = 7
CODE_LENGTH = 6
CODE_ALPHABET = string.ascii_uppercase + string.digits


class FriendshipService:

    # -------- helpers --------

    @staticmethod
    def _generate_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def _generate_unique_code(db: Session) -> str:
        for _ in range(10):
            code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
            existing = db.query(FriendInvite).filter(FriendInvite.code == code).first()
            if not existing:
                return code
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo generar un código único, inténtalo de nuevo"
        )

    @staticmethod
    def _are_friends(db: Session, user_a_id: int, user_b_id: int) -> bool:
        existing = db.query(Friendship).filter(
            or_(
                and_(Friendship.requester_id == user_a_id, Friendship.addressee_id == user_b_id),
                and_(Friendship.requester_id == user_b_id, Friendship.addressee_id == user_a_id),
            ),
            Friendship.status == FriendshipStatus.accepted,
        ).first()
        return existing is not None

    # -------- invites --------

    @staticmethod
    def create_invite(db: Session, user: User) -> FriendInvite:
        invite = FriendInvite(
            token=FriendshipService._generate_token(),
            code=FriendshipService._generate_unique_code(db),
            inviter_id=user.id,
            expires_at=datetime.now() + timedelta(days=INVITE_EXPIRY_DAYS),
        )
        db.add(invite)
        db.commit()
        db.refresh(invite)
        return invite

    @staticmethod
    def list_invites(db: Session, user: User) -> list[FriendInvite]:
        """Devuelve invites activos del usuario (no usados y no caducados)."""
        now = datetime.now()
        return db.query(FriendInvite).filter(
            FriendInvite.inviter_id == user.id,
            FriendInvite.used_at.is_(None),
            FriendInvite.expires_at > now,
        ).order_by(FriendInvite.created_at.desc()).all()

    @staticmethod
    def delete_invite(db: Session, user: User, invite_id: int) -> None:
        invite = db.query(FriendInvite).filter(FriendInvite.id == invite_id).first()
        if not invite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitación no encontrada"
            )
        if invite.inviter_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes borrar una invitación ajena"
            )
        db.delete(invite)
        db.commit()

    @staticmethod
    def lookup_invite_by_code(db: Session, code: str) -> dict:
        invite = db.query(FriendInvite).filter(FriendInvite.code == code.upper()).first()
        if not invite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código no encontrado"
            )
        is_valid = invite.used_at is None and invite.expires_at > datetime.now()
        return {
            "code": invite.code,
            "inviter": invite.inviter,
            "expires_at": invite.expires_at,
            "is_valid": is_valid,
        }

    @staticmethod
    def accept_invite(db: Session, user: User, token: str) -> Friendship:
        invite = db.query(FriendInvite).filter(FriendInvite.token == token).first()
        if not invite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invitación no encontrada"
            )
        if invite.used_at is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta invitación ya ha sido usada"
            )
        if invite.expires_at < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esta invitación ha caducado"
            )
        if invite.inviter_id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes aceptar tu propia invitación"
            )
        if FriendshipService._are_friends(db, invite.inviter_id, user.id):
            # Marcamos invite como usado igualmente para que no quede activo
            invite.used_at = datetime.now()
            invite.used_by_id = user.id
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya sois amigos"
            )

        # Crear friendship aceptada
        now = datetime.now()
        friendship = Friendship(
            requester_id=invite.inviter_id,
            addressee_id=user.id,
            status=FriendshipStatus.accepted,
            responded_at=now,
        )
        invite.used_at = now
        invite.used_by_id = user.id
        db.add(friendship)
        db.commit()
        db.refresh(friendship)
        return friendship

    # -------- friends --------

    @staticmethod
    def list_friends(db: Session, user: User) -> list[Friendship]:
        """Devuelve todas las friendships aceptadas donde el user es parte."""
        return db.query(Friendship).filter(
            or_(
                Friendship.requester_id == user.id,
                Friendship.addressee_id == user.id,
            ),
            Friendship.status == FriendshipStatus.accepted,
        ).all()

    @staticmethod
    def remove_friend(db: Session, user: User, other_user_id: int) -> None:
        friendship = db.query(Friendship).filter(
            or_(
                and_(Friendship.requester_id == user.id, Friendship.addressee_id == other_user_id),
                and_(Friendship.requester_id == other_user_id, Friendship.addressee_id == user.id),
            ),
            Friendship.status == FriendshipStatus.accepted,
        ).first()
        if not friendship:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No sois amigos"
            )
        db.delete(friendship)
        db.commit()
        
    @staticmethod
    def accept_invite_by_code(db: Session, user: User, code: str) -> Friendship:
        invite = db.query(FriendInvite).filter(FriendInvite.code == code.upper()).first()
        if not invite:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Código no encontrado"
            )
        return FriendshipService.accept_invite(db, user, invite.token)


