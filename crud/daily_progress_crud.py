from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Date, cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.daily_progress import DailyProgress
from openapi.db.schemas.daily_progress import DailyProgressCreate, DailyProgressUpdate


class DailyProgressCRUD:
    """
    CRUD-операції для DailyProgress.
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: DailyProgressCreate) -> DailyProgress:
        """
        Створити новий запис щоденного прогресу.
        """
        db_obj = DailyProgress(
            user_id=user_id,
            date=obj_in.date,
            words_learned=obj_in.words_learned,
            words_reviewed=obj_in.words_reviewed,
            test_sessions_passed=obj_in.test_sessions_passed,
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Цей прогрес вже існує для цього дня."
            )
        return db_obj

    @staticmethod
    def get(db: Session, progress_id: UUID, user_id: UUID) -> DailyProgress:
        """
        Отримати запис прогресу по id (перевіряємо user_id для безпеки).
        """
        stmt = select(DailyProgress).where(
            DailyProgress.id == progress_id,
            DailyProgress.user_id == user_id,
            DailyProgress.deleted_at.is_(None),
        )
        result = db.execute(stmt).scalar_one_or_none()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Прогрес не знайдено."
            )
        return result

    @staticmethod
    def get_all(db: Session, user_id: UUID) -> list[DailyProgress]:
        """
        Отримати всі записи прогресу користувача (тільки не видалені).
        """
        stmt = (
            select(DailyProgress)
            .where(DailyProgress.user_id == user_id, DailyProgress.deleted_at.is_(None))
            .order_by(DailyProgress.date.desc())
        )
        result = db.execute(stmt).scalars().all()
        return result

    @staticmethod
    def update(
        db: Session, progress_id: UUID, user_id: UUID, obj_in: DailyProgressUpdate
    ) -> DailyProgress:
        """
        Оновити запис прогресу (partial update, тільки свої поля).
        """
        db_obj = DailyProgressCRUD.get(db, progress_id, user_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def soft_delete(db: Session, progress_id: UUID, user_id: UUID) -> None:
        """
        М'яке видалення запису — ставимо deleted_at.
        """
        db_obj = DailyProgressCRUD.get(db, progress_id, user_id)
        db_obj.deleted_at = datetime.now(timezone.utc)
        db.commit()

    @staticmethod
    def get_by_user_and_date(db: Session, user_id: UUID, date: datetime) -> Optional[DailyProgress]:
        """
        Повертає запис прогресу для конкретного користувача на конкретну дату (UTC).
        """
        stmt = select(DailyProgress).where(
            DailyProgress.user_id == user_id,
            cast(DailyProgress.date, Date) == date.date(),
            DailyProgress.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()
