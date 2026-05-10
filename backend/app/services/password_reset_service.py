import secrets
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.models.password_reset import PasswordReset
from app.models.user import User


class PasswordResetService:

    @staticmethod
    def create_token(db: Session, user: User) -> str:
        # Invalida tokens anteriores del usuario
        db.query(PasswordReset).filter(
            PasswordReset.user_id == user.id,
            PasswordReset.used.is_(False),
        ).update({"used": True})

        token = secrets.token_urlsafe(32)
        reset = PasswordReset(
            user_id=user.id,
            token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        db.add(reset)
        db.commit()
        return token

    @staticmethod
    def get_valid_token(db: Session, token: str) -> PasswordReset | None:
        reset = db.query(PasswordReset).filter(
            PasswordReset.token == token,
            PasswordReset.used.is_(False),
        ).first()
        if not reset:
            return None
        if reset.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return None
        return reset

    @staticmethod
    def consume_token(db: Session, reset: PasswordReset, new_password: str):
        from app.services.user_service import UserService
        UserService.set_password(db, reset.user, new_password)
        reset.used = True
        db.commit()
