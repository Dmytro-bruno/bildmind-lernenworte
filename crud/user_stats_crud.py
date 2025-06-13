from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.user_stats import UserStats
from openapi.db.schemas.user_stats import UserStatsCreate, UserStatsUpdate


class UserStatsCRUD:
    """
    CRUD-операції для UserStats (статистика користувача).
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: UserStatsCreate) -> UserStats:
        """
        Створити статистику для користувача.
        """
        # Дозволяємо лише 1 запис статистики на user_id
        stmt = select(UserStats).where(UserStats.user_id == user_id, UserStats.deleted_at.is_(None))
        existing = db.execute(stmt).scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Статистика для цього користувача вже існує.",
            )
        db_obj = UserStats(
            user_id=user_id,
            words_learned=obj_in.words_learned,
            words_in_progress=obj_in.words_in_progress,
            test_sessions_total=obj_in.test_sessions_total,
            test_sessions_passed=obj_in.test_sessions_passed,
            last_active=obj_in.last_active or datetime.now(timezone.utc),
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
                detail="Конфлікт під час створення статистики.",
            )
        return db_obj

    @staticmethod
    def get_by_user(db: Session, user_id: UUID) -> Optional[UserStats]:
        """
        Отримати статистику за user_id (лише не видалені).
        """
        stmt = select(UserStats).where(
            UserStats.user_id == user_id,
            UserStats.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def update(db: Session, user_id: UUID, obj_in: UserStatsUpdate) -> UserStats:
        """
        Оновити статистику користувача (partial update).
        """
        db_obj = UserStatsCRUD.get_by_user(db, user_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Статистика користувача не знайдена."
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
        М'яке видалення статистики — ставить deleted_at.
        """
        db_obj = UserStatsCRUD.get_by_user(db, user_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Статистика користувача не знайдена."
            )
        db_obj.deleted_at = datetime.now(timezone.utc)
        db.commit()
