from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status


class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Obtener usuario por email"""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Obtener usuario por nombre de usuario"""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Obtener usuario por ID"""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Crear un nuevo usuario"""
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email, username=user.username, hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """Obtener todos los usuarios"""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user: User, data: UserUpdate) -> User:
        """Actualizar email y/o username del usuario"""
        if data.email is not None and data.email != user.email:
            existing = UserService.get_user_by_email(db, data.email)
            if existing and existing.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está en uso",
                )
            user.email = data.email

        if data.username is not None and data.username != user.username:
            existing = UserService.get_user_by_username(db, data.username)
            if existing and existing.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El username ya está en uso",
                )
            user.username = data.username

        if (
            data.share_location is not None
            and data.share_location != user.share_location
        ):
            user.share_location = data.share_location

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def change_password(
        db: Session, user: User, current_password: str, new_password: str
    ) -> None:
        """Cambiar contraseña verificando la actual"""
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña actual es incorrecta",
            )

        if verify_password(new_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La nueva contraseña debe ser distinta de la actual",
            )

        user.hashed_password = get_password_hash(new_password)
        db.commit()

    @staticmethod
    def deactivate_user(db: Session, user: User) -> None:
        """Soft delete: marcar usuario como inactivo"""
        if not user.is_active:
            return
        user.is_active = False
        db.commit()
