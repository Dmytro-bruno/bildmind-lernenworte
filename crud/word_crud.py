from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.word import Word
from openapi.db.schemas.word import WordCreate, WordUpdate


class WordCRUD:
    """
    CRUD-операції для Word (загальний словник слів).
    """

    @staticmethod
    def create(db: Session, obj_in: WordCreate) -> Word:
        """
        Додати нове слово у словник.
        """
        db_obj = Word(
            base_form=obj_in.base_form,
            article=obj_in.article,
            base_and_article=obj_in.base_and_article,
            translation=obj_in.translation,
            lang_from=obj_in.lang_from,
            lang_to=obj_in.lang_to,
            example=obj_in.example,
            created_at=datetime.now(timezone.utc),
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
                detail="Таке слово вже існує або порушено унікальність.",
            )
        return db_obj

    @staticmethod
    def get_by_id(db: Session, word_id: UUID) -> Optional[Word]:
        """
        Отримати слово по id (не видалене).
        """
        stmt = select(Word).where(
            Word.id == word_id,
            Word.deleted_at.is_(None),
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Word]:
        """
        Отримати всі слова зі словника (не видалені).
        """
        stmt = (
            select(Word)
            .where(Word.deleted_at.is_(None))
            .order_by(Word.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update(db: Session, word_id: UUID, obj_in: WordUpdate) -> Word:
        """
        Оновити слово у словнику (partial update).
        """
        db_obj = WordCRUD.get_by_id(db, word_id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слово не знайдено.")
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def soft_delete(db: Session, word_id: UUID) -> None:
        """
        М'яке видалення слова — ставить deleted_at.
        """
        db_obj = WordCRUD.get_by_id(db, word_id)
        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слово не знайдено.")
        db_obj.deleted_at = datetime.now(timezone.utc)
        db.commit()
