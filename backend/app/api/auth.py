from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, PasswordChange
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.deps import get_current_active_user
from app.models.user import User
from fastapi import Request
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/hour")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    # Verificar si el email ya está registrado
    db_user = UserService.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado",
        )

    # Verificar si el username ya existe
    db_user = UserService.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El username ya existe"
        )

    # Crear el usuario
    new_user = UserService.create_user(db, user)
    return new_user


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    """Iniciar sesión y obtener token de acceso"""
    # Autenticar usuario
    user = AuthService.authenticate_user(db, credentials)
    # Crear token de acceso
    access_token = AuthService.create_token(user.email)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user=Depends(get_current_active_user)):
    """Obtener información del usuario actual"""
    return current_user


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/hour")
def change_password(
    request: Request,
    data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Cambiar la contraseña del usuario autenticado"""
    UserService.change_password(
        db=db,
        user=current_user,
        current_password=data.current_password,
        new_password=data.new_password,
    )
