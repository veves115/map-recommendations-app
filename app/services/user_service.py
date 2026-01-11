from unittest import skip
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

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
            user_email=user.email,
            username=user.username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_all_users(db: Session) -> list[User]:
        """Obtener todos los usuarios"""
        return db.query(User).offset(skip).limit(limit).all()
    
     