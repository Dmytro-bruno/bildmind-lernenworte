from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.user_stats_crud import UserStatsCRUD
from openapi.db.models.user import User
from openapi.db.schemas.user_stats import UserStatsCreate, UserStatsRead, UserStatsUpdate

router = APIRouter(
    prefix="/user-stats",
    tags=["User Stats"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=UserStatsRead, summary="Отримати статистику поточного користувача")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає статистику лише для поточного користувача.
    """
    stats = UserStatsCRUD.get_by_user(db, user_id=current_user.id)
    if not stats:
        raise HTTPException(status_code=404, detail="Статистика не знайдена")
    return stats


@router.post(
    "",
    response_model=UserStatsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Створити статистику для поточного користувача",
)
def create_user_stats(
    data: UserStatsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Створює статистику лише для поточного користувача.
    """
    return UserStatsCRUD.create(db, user_id=current_user.id, obj_in=data)


@router.patch("", response_model=UserStatsRead, summary="Оновити статистику поточного користувача")
def update_user_stats(
    data: UserStatsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює статистику лише для поточного користувача.
    """
    return UserStatsCRUD.update(db, user_id=current_user.id, obj_in=data)


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити (soft) статистику поточного користувача",
)
def delete_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    М'яко видаляє статистику лише для поточного користувача.
    """
    UserStatsCRUD.soft_delete(db, user_id=current_user.id)
    return None
