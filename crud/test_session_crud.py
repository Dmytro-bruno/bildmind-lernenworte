from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.test_session import TestSession  # SQLAlchemy модель
from openapi.db.schemas.test_session import TestSessionCreate, TestSessionUpdate


class TestSessionCRUD:
    """
    CRUD-операції для TestSession.
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: TestSessionCreate) -> TestSession:
        """
        Створити нову сесію тестування.
        """
        db_obj = TestSession(
            user_id=user_id,
            start_time=obj_in.start_time,
            end_time=obj_in.end_time,
            words_total=obj_in.words_total,
            correct=obj_in.correct,
            test_type=obj_in.test_type,
            deleted_at=None,
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Така сесія тестування вже існує."
            )
        return db_obj

    @staticmethod
    def get(db: Session, session_id: UUID, user_id: UUID) -> TestSession:
        """
        Отримати сесію тестування по id (з перевіркою user_id і видалення).
        """
        stmt = select(TestSession).where(
            TestSession.id == session_id,
            TestSession.user_id == user_id,
            TestSession.deleted_at.is_(None),
        )
        result = db.execute(stmt).scalar_one_or_none()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Сесія тестування не знайдена."
            )
        return result  # тут уже точно не None, бо raise!

    @staticmethod
    def get_all(db: Session, user_id: UUID) -> list[TestSession]:
        """
        Отримати всі активні сесії тестування користувача.
        """
        stmt = (
            select(TestSession)
            .where(
                TestSession.user_id == user_id,
                TestSession.deleted_at.is_(None),
            )
            .order_by(TestSession.start_time.desc())
        )
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update(
        db: Session, session_id: UUID, user_id: UUID, obj_in: TestSessionUpdate
    ) -> TestSession:
        """
        Оновити сесію тестування (partial update).
        """
        db_obj = TestSessionCRUD.get(db, session_id, user_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def soft_delete(db: Session, session_id: UUID, user_id: UUID) -> None:
        """
        М'яке видалення сесії тестування — ставимо deleted_at.
        """
        db_obj = TestSessionCRUD.get(db, session_id, user_id)
        db_obj.deleted_at = datetime.now(timezone.utc)
        db.commit()
