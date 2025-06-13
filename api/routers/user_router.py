from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user
from openapi.crud.user_crud import delete_user, get_user_by_id, get_users, update_user
from openapi.db.models.user import User
from openapi.db.schemas.user import UserRead, UserUpdate
from openapi.db.session import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[UserRead], summary="Отримати всіх користувачів")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає всіх активних користувачів (тільки адміну).
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Недостатньо прав")
    return get_users(db)


@router.get("/{user_id}", response_model=UserRead, summary="Отримати користувача за id")
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає користувача по id (себе або тільки адміну).
    """
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Доступ лише до свого профілю або адміну")
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return user


@router.patch("/{user_id}", response_model=UserRead, summary="Оновити користувача")
def update_user_endpoint(
    user_id: UUID,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює профіль користувача (тільки свій або адміну).
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Доступ лише до свого профілю або адміну")
    return update_user(db, user, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити користувача (soft-delete)",
)
def delete_user_endpoint(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    М'яко видаляє користувача (тільки себе або адміну).
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Доступ лише до свого профілю або адміну")
    delete_user(db, user)
    return None
