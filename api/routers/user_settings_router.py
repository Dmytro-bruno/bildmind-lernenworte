from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from openapi.api.routers.dependencies import get_current_user, get_db
from openapi.crud.user_settings_crud import UserSettingsCRUD
from openapi.db.schemas.user_settings import (
    UserSettingsCreate,
    UserSettingsRead,
    UserSettingsUpdate,
)

router = APIRouter(prefix="/user_settingss", tags=["UserSettings"])


@router.get("/", response_model=List[UserSettingsRead])
def read_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return UserSettingsCRUD.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=UserSettingsRead)
def create(
    obj_in: UserSettingsCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return UserSettingsCRUD.create(db, obj_in)


@router.get("/{id}", response_model=UserSettingsRead)
def read_one(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = UserSettingsCRUD.get(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{id}", response_model=UserSettingsRead)
def update(
    id: str,
    obj_in: UserSettingsUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_obj = UserSettingsCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserSettingsCRUD.update(db, db_obj, obj_in)


@router.delete("/{id}", response_model=UserSettingsRead)
def delete(id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_obj = UserSettingsCRUD.get(db, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Not found")
    return UserSettingsCRUD.delete(db, db_obj)
