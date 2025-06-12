from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from openapi.crud.user_crud import authenticate_user, create_user, get_user_by_email
from openapi.db.schemas.token import LoginRequest, TokenResponse
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
    token = create_access_token({"sub": str(user.id)})
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
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, token_type="bearer")  # nosec
