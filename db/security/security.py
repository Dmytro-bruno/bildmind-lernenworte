from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from openapi.config.settings import settings
from openapi.db.models.user import User
from openapi.db.session import get_db

# --- Паролі ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Хешує пароль користувача для зберігання у БД.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє, чи співпадає plain-пароль із його хешем.
    """
    return pwd_context.verify(plain_password, hashed_password)


# --- JWT ---
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # заміни, якщо інший шлях


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Створює JWT access token із payload та часом життя.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Декодує access token і повертає payload, або піднімає HTTPException при помилці.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не вдалось перевірити токен.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """
    Дістає user_id (sub) з access token. Повертає user_id або піднімає помилку.
    """
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None or not isinstance(user_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Користувача не знайдено або токен недійсний.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    Дістає об'єкт User з БД за токеном авторизації.
    """
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None or not isinstance(user_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недійсний токен (user_id не знайдено)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Користувача не знайдено або він видалений.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
