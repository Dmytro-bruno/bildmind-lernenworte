from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.user_settings import UserSettings
from openapi.db.schemas.user_settings import UserSettingsCreate, UserSettingsUpdate


class UserSettingsCRUD:
    """
    CRUD-операції для UserSettings (налаштування користувача).
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: UserSettingsCreate) -> UserSettings:
        """
        Створити налаштування для користувача.
        """
        # Дозволяємо лише 1 запис налаштувань на user_id
        stmt = select(UserSettings).where(
            UserSettings.user_id == user_id, UserSettings.deleted_at.is_(None)
        )
        existing = db.execute(stmt).scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Налаштування для цього користувача вже існують.",
            )
        db_obj = UserSettings(
            user_id=user_id,
            interface_language=obj_in.interface_language,
            native_language=obj_in.native_language,
            target_language=obj_in.target_language,
            notifications_enabled=obj_in.notifications_enabled,
            dark_mode=obj_in.dark_mode,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            deleted_at=None,
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Конфлікт під час створення налаштувань.",
            )
        return db_obj

    @staticmethod
    def get_by_user(db: Session, user_id: UUID) -> Optional[UserSettings]:
        """
        Отримати налаштування за user_id (лише не видалені).
        """
        stmt = select(UserSettings).where(
            UserSettings.user_id == user_id,
            UserSettings.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def update(db: Session, user_id: UUID, obj_in: UserSettingsUpdate) -> UserSettings:
        """
        Оновити налаштування користувача (partial update).
        """
        db_obj = UserSettingsCRUD.get_by_user(db, user_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Налаштування користувача не знайдено.",
            )
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db_obj.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def soft_delete(db: Session, user_id: UUID) -> None:
        """
        М'яке видалення налаштувань — ставить deleted_at.
        """
        db_obj = UserSettingsCRUD.get_by_user(db, user_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Налаштування користувача не знайдено.",
            )
        db_obj.deleted_at = datetime.now(timezone.utc)
        db.commit()
