from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.orm import Session

from core.services.token_blacklist_service import TokenBlacklistService
from openapi.api.routers.dependencies import bearer_scheme, get_current_user
from openapi.config.settings import settings
from openapi.crud.user_crud import authenticate_user, create_user, get_user_by_email
from openapi.db.models.user import User
from openapi.db.schemas.token import LoginRequest, TokenResponse
from openapi.db.schemas.token_blacklist import TokenBlacklistCreate
from openapi.db.schemas.user import UserCreate
from openapi.db.security.security import create_access_token
from openapi.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, summary="Реєстрація нового користувача")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Реєстрація нового користувача, повертає access_token.
    """
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email вже зареєстровано")
    user = create_user(db, user_in)
    jti = str(uuid4())
    token = create_access_token({"sub": str(user.id), "jti": jti})
    return TokenResponse(access_token=token, token_type="bearer")  # nosec


@router.post("/login", response_model=TokenResponse, summary="Логін користувача")
def login(login_in: LoginRequest, db: Session = Depends(get_db)):
    """
    Логін користувача за email та паролем, повертає access_token.
    """
    user = authenticate_user(db, login_in.email, login_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Невірна пошта або пароль"
        )
    jti = str(uuid4())
    token = create_access_token({"sub": str(user.id), "jti": jti})
    return TokenResponse(access_token=token, token_type="bearer")  # nosec


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Вихід користувача")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Вихід користувача. Токен додається у чорний список.
    """
    token = credentials.credentials
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    jti = payload.get("jti")
    exp = payload.get("exp")

    if jti:
        TokenBlacklistService.add_token_to_blacklist(
            db=db,
            user_id=current_user.id,
            obj_in=TokenBlacklistCreate(
                jti=jti,
                expired_at=datetime.fromtimestamp(exp, tz=timezone.utc),
                reason="User logout",
            ),
        )
