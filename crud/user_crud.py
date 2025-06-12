from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from openapi.db.models.user import User
from openapi.db.schemas.user import UserCreate, UserUpdate
from openapi.db.security.security import (  # додати verify_password
    get_password_hash,
    verify_password,
)


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """Повертає користувача по id або None, якщо не знайдено."""
    return db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Повертає користувача по email або None, якщо не знайдено."""
    return db.query(User).filter(User.email == email, User.deleted_at.is_(None)).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Повертає користувача по username або None, якщо не знайдено."""
    return db.query(User).filter(User.username == username, User.deleted_at.is_(None)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Повертає список усіх активних користувачів (не видалених)."""
    return db.query(User).filter(User.deleted_at.is_(None)).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    """Створює користувача з хешованим паролем. Захищає від дублікатів email/username."""
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Користувач з таким email або username вже існує.",
        )
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    """Оновлює користувача: email, username, пароль (з хешуванням)."""
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.username is not None:
        user.username = user_in.username
    if user_in.password is not None:
        user.hashed_password = get_password_hash(user_in.password)
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email або username вже зайнятий іншим користувачем.",
        )
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> User:
    """М'яке видалення користувача: проставляє дату видалення."""
    user.deleted_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Перевіряє правильність email та пароля. Повертає User якщо все вірно, або None.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
