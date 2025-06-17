from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.services.token_blacklist_service import TokenBlacklistService
from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.db.models.user import User
from openapi.db.schemas.token_blacklist import (
    TokenBlacklistCreate,
    TokenBlacklistRead,
    TokenBlacklistUpdate,
)

router = APIRouter(
    prefix="/token-blacklist",
    tags=["Token Blacklist"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=TokenBlacklistRead,
    status_code=status.HTTP_201_CREATED,
    summary="Додати токен у чорний список",
)
def create_token_blacklist(
    data: TokenBlacklistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Додає токен у чорний список для поточного користувача.
    """
    return TokenBlacklistService.create(db, user_id=current_user.id, obj_in=data)


@router.get(
    "/{blacklist_id}",
    response_model=TokenBlacklistRead,
    summary="Отримати запис з чорного списку за id",
)
def get_token_blacklist(
    blacklist_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає запис з чорного списку поточного користувача.
    """
    return TokenBlacklistService.get(db, blacklist_id=blacklist_id, user_id=current_user.id)


@router.get(
    "",
    response_model=List[TokenBlacklistRead],
    summary="Отримати всі записи чорного списку користувача",
)
def list_token_blacklist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає список усіх записів чорного списку користувача.
    """
    return TokenBlacklistService.get_all(db, user_id=current_user.id)


@router.patch(
    "/{blacklist_id}", response_model=TokenBlacklistRead, summary="Оновити запис чорного списку"
)
def update_token_blacklist(
    blacklist_id: UUID,
    data: TokenBlacklistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює запис чорного списку.
    """
    return TokenBlacklistService.update(
        db, blacklist_id=blacklist_id, user_id=current_user.id, obj_in=data
    )


@router.delete(
    "/{blacklist_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити запис чорного списку",
)
def delete_token_blacklist(
    blacklist_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Видаляє запис чорного списку (повністю).
    """
    TokenBlacklistService.delete(db, blacklist_id=blacklist_id, user_id=current_user.id)
    return None
