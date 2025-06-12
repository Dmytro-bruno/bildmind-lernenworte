from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.user_settings_crud import UserSettingsCRUD
from openapi.db.models.user import User
from openapi.db.schemas.user_settings import (
    UserSettingsCreate,
    UserSettingsRead,
    UserSettingsUpdate,
)

router = APIRouter(
    prefix="/user-settings",
    tags=["User Settings"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "", response_model=UserSettingsRead, summary="Отримати налаштування поточного користувача"
)
def get_user_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Повертає налаштування лише для поточного користувача.
    """
    settings = UserSettingsCRUD.get_by_user(db, user_id=current_user.id)
    if not settings:
        raise HTTPException(status_code=404, detail="Налаштування не знайдено")
    return settings


@router.post(
    "",
    response_model=UserSettingsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Створити налаштування для поточного користувача",
)
def create_user_settings(
    data: UserSettingsCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Створює налаштування лише для поточного користувача.
    """
    return UserSettingsCRUD.create(db, user_id=current_user.id, obj_in=data)


@router.patch(
    "", response_model=UserSettingsRead, summary="Оновити налаштування поточного користувача"
)
def update_user_settings(
    data: UserSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Оновлює налаштування лише для поточного користувача.
    """
    return UserSettingsCRUD.update(db, user_id=current_user.id, obj_in=data)


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити (soft) налаштування поточного користувача",
)
def delete_user_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    М'яко видаляє налаштування лише для поточного користувача.
    """
    UserSettingsCRUD.soft_delete(db, user_id=current_user.id)
    return None
