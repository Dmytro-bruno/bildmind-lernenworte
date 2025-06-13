from datetime import datetime, timezone
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.gpt_logs import GPTLog  # твоя модель SQLAlchemy
from openapi.db.schemas.gpt_logs import GPTLogCreate, GPTLogUpdate


class GPTLogsCRUD:
    """
    CRUD-операції для логування GPT-запитів.
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: GPTLogCreate) -> GPTLog:
        """
        Створити новий GPT-log для користувача.
        """
        db_obj = GPTLog(
            user_id=user_id,
            prompt=obj_in.prompt,
            response=obj_in.response,
            token_usage=obj_in.token_usage,
            word_id=obj_in.word_id,
            timestamp=datetime.now(timezone.utc),
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Помилка створення логу (можливий дублікат або помилка даних).",
            )
        return db_obj

    @staticmethod
    def get(db: Session, log_id: UUID, user_id: UUID) -> GPTLog:
        """
        Отримати GPT-log по id (для поточного користувача).
        """
        stmt = select(GPTLog).where(
            and_(
                GPTLog.id == log_id,
                GPTLog.user_id == user_id,
            )
        )
        result = db.execute(stmt).scalar_one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Лог не знайдено.")
        return result

    @staticmethod
    def get_all(db: Session, user_id: UUID) -> List[GPTLog]:
        """
        Отримати всі логи користувача, новіші — першими.
        """
        stmt = select(GPTLog).where(GPTLog.user_id == user_id).order_by(GPTLog.timestamp.desc())
        result = db.execute(stmt).scalars().all()
        return result

    @staticmethod
    def update(db: Session, log_id: UUID, user_id: UUID, obj_in: GPTLogUpdate) -> GPTLog:
        """
        Оновити GPT-log (partial update, тільки свої поля).
        """
        db_obj = GPTLogsCRUD.get(db, log_id, user_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, log_id: UUID, user_id: UUID) -> None:
        """
        Жорстке видалення лог-запису GPT (повністю з БД).
        """
        db_obj = GPTLogsCRUD.get(db, log_id, user_id)
        db.delete(db_obj)
        db.commit()
