from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.daily_progress_crud import DailyProgressCRUD
from openapi.db.models.user import User  # твоя модель користувача
from openapi.db.schemas.daily_progress import (
    DailyProgressCreate,
    DailyProgressRead,
    DailyProgressUpdate,
)

router = APIRouter(
    prefix="/daily-progress",
    tags=["Daily Progress"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=DailyProgressRead,
    status_code=status.HTTP_201_CREATED,
    summary="Створити запис щоденного прогресу",
)
def create_daily_progress(
    data: DailyProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Додає новий запис прогресу для поточного користувача.
    """
    return DailyProgressCRUD.create(db, user_id=current_user.id, obj_in=data)


@router.get(
    "/{progress_id}",
    response_model=DailyProgressRead,
    summary="Отримати запис прогресу за id",
)
def get_daily_progress(
    progress_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає конкретний запис прогресу поточного користувача.
    """
    return DailyProgressCRUD.get(db, progress_id=progress_id, user_id=current_user.id)


@router.get(
    "",
    response_model=List[DailyProgressRead],
    summary="Отримати всі записи прогресу для поточного користувача",
)
def list_daily_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає список всіх записів прогресу користувача (не видалені).
    """
    return DailyProgressCRUD.get_all(db, user_id=current_user.id)


@router.patch(
    "/{progress_id}",
    response_model=DailyProgressRead,
    summary="Оновити запис прогресу (partial update)",
)
def update_daily_progress(
    progress_id: UUID,
    data: DailyProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює існуючий запис прогресу (тільки свої).
    """
    return DailyProgressCRUD.update(
        db, progress_id=progress_id, user_id=current_user.id, obj_in=data
    )


@router.delete(
    "/{progress_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="М'яке видалення запису прогресу",
)
def delete_daily_progress(
    progress_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    М'яко видаляє запис прогресу (ставить deleted_at).
    """
    DailyProgressCRUD.soft_delete(db, progress_id=progress_id, user_id=current_user.id)
    return None
