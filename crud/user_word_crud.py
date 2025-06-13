from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.user_word import UserWord
from openapi.db.schemas.user_word import UserWordCreate, UserWordUpdate


class UserWordCRUD:
    """
    CRUD-операції для UserWord (слова у словнику користувача).
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: UserWordCreate) -> UserWord:
        """
        Додати слово у словник користувача.
        """
        # Не дозволяємо дублікати word_id+user_id серед не видалених
        stmt = select(UserWord).where(
            UserWord.user_id == user_id,
            UserWord.word_id == obj_in.word_id,
            UserWord.deleted_at.is_(None),
        )
        existing = db.execute(stmt).scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Слово вже є у словнику користувача."
            )
        db_obj = UserWord(
            user_id=user_id,
            word_id=obj_in.word_id,
            level=obj_in.level,
            next_review_date=obj_in.next_review_date,
            last_review_date=obj_in.last_review_date,
            is_learned=obj_in.is_learned,
            success_count=obj_in.success_count,
            fail_count=obj_in.fail_count,
            note=obj_in.note,
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
                status_code=status.HTTP_409_CONFLICT, detail="Конфлікт під час додавання слова."
            )
        return db_obj

    @staticmethod
    def get_by_id(db: Session, user_id: UUID, user_word_id: UUID) -> Optional[UserWord]:
        """
        Отримати слово з особистого словника по id (user_id).
        """
        stmt = select(UserWord).where(
            UserWord.id == user_word_id,
            UserWord.user_id == user_id,
            UserWord.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_by_word(db: Session, user_id: UUID, word_id: UUID) -> Optional[UserWord]:
        """
        Отримати слово за user_id+word_id (уникати дублікатів).
        """
        stmt = select(UserWord).where(
            UserWord.user_id == user_id,
            UserWord.word_id == word_id,
            UserWord.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(db: Session, user_id: UUID) -> List[UserWord]:
        """
        Отримати всі слова зі словника користувача.
        """
        stmt = (
            select(UserWord)
            .where(
                UserWord.user_id == user_id,
                UserWord.deleted_at.is_(None),
            )
            .order_by(UserWord.created_at.desc())
        )
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update(db: Session, user_id: UUID, user_word_id: UUID, obj_in: UserWordUpdate) -> UserWord:
        """
        Оновити слово зі словника (partial update).
        """
        db_obj = UserWordCRUD.get_by_id(db, user_id, user_word_id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слово не знайдено.")
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db_obj.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def soft_delete(db: Session, user_id: UUID, user_word_id: UUID) -> None:
        """
        М'яке видалення слова — ставить deleted_at.
        """
        db_obj = UserWordCRUD.get_by_id(db, user_id, user_word_id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слово не знайдено.")
        db_obj.deleted_at = datetime.now(timezone.utc)
        db.commit()
