from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.level_progress import LevelProgress
from openapi.db.schemas.level_progress import LevelProgressCreate, LevelProgressUpdate


class LevelProgressCRUD:
    """
    CRUD-операції для LevelProgress (прогрес по рівнях).
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: LevelProgressCreate) -> LevelProgress:
        """
        Створити новий запис прогресу по рівню.
        """
        db_obj = LevelProgress(
            user_id=user_id,
            word_level=obj_in.word_level,
            words_learned=obj_in.words_learned,
            accuracy=obj_in.accuracy,
            last_interaction=obj_in.last_interaction or datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Такий запис вже існує для цього рівня.",
            )
        return db_obj

    @staticmethod
    def get(db: Session, progress_id: UUID, user_id: UUID) -> LevelProgress:
        """
        Отримати прогрес по id (з перевіркою user_id).
        """
        stmt = select(LevelProgress).where(
            LevelProgress.id == progress_id,
            LevelProgress.user_id == user_id,
        )
        result = db.execute(stmt).scalar_one_or_none()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Прогрес по рівню не знайдено."
            )
        return result

    @staticmethod
    def get_all(db: Session, user_id: UUID) -> list[LevelProgress]:
        """
        Отримати всі записи прогресу по рівнях користувача.
        """
        stmt = (
            select(LevelProgress)
            .where(LevelProgress.user_id == user_id)
            .order_by(LevelProgress.word_level)
        )
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update(
        db: Session, progress_id: UUID, user_id: UUID, obj_in: LevelProgressUpdate
    ) -> LevelProgress:
        """
        Оновити прогрес по рівню (partial update).
        """
        db_obj = LevelProgressCRUD.get(db, progress_id, user_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db_obj.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, progress_id: UUID, user_id: UUID) -> None:
        """
        Жорстке видалення прогресу по рівню.
        """
        db_obj = LevelProgressCRUD.get(db, progress_id, user_id)
        db.delete(db_obj)
        db.commit()
