from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.level_progress_crud import LevelProgressCRUD
from openapi.db.models.user import User
from openapi.db.schemas.level_progress import (
    LevelProgressCreate,
    LevelProgressRead,
    LevelProgressUpdate,
)

router = APIRouter(
    prefix="/level-progress",
    tags=["Level Progress"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=LevelProgressRead,
    status_code=status.HTTP_201_CREATED,
    summary="Створити запис прогресу по рівню",
)
def create_level_progress(
    data: LevelProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Додає новий запис прогресу по рівню для поточного користувача.
    """
    return LevelProgressCRUD.create(db, user_id=current_user.id, obj_in=data)


@router.get(
    "/{progress_id}",
    response_model=LevelProgressRead,
    summary="Отримати запис прогресу по рівню за id",
)
def get_level_progress(
    progress_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає конкретний запис прогресу по рівню поточного користувача.
    """
    return LevelProgressCRUD.get(db, progress_id=progress_id, user_id=current_user.id)


@router.get(
    "", response_model=List[LevelProgressRead], summary="Отримати всі записи прогресу по рівнях"
)
def list_level_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає список всіх записів прогресу по рівнях користувача.
    """
    return LevelProgressCRUD.get_all(db, user_id=current_user.id)


@router.patch(
    "/{progress_id}", response_model=LevelProgressRead, summary="Оновити запис прогресу по рівню"
)
def update_level_progress(
    progress_id: UUID,
    data: LevelProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює існуючий запис прогресу по рівню (partial update).
    """
    return LevelProgressCRUD.update(
        db, progress_id=progress_id, user_id=current_user.id, obj_in=data
    )


@router.delete(
    "/{progress_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити запис прогресу по рівню",
)
def delete_level_progress(
    progress_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Видаляє запис прогресу по рівню (тільки свої).
    """
    LevelProgressCRUD.delete(db, progress_id=progress_id, user_id=current_user.id)
    return None
