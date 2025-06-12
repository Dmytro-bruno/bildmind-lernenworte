from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from openapi.db.models.token_blacklist import TokenBlacklist
from openapi.db.schemas.token_blacklist import TokenBlacklistCreate, TokenBlacklistUpdate


class TokenBlacklistCRUD:
    """
    CRUD-операції для TokenBlacklist (JWT чорний список).
    """

    @staticmethod
    def create(db: Session, user_id: UUID, obj_in: TokenBlacklistCreate) -> TokenBlacklist:
        """
        Додати токен у чорний список.
        """
        db_obj = TokenBlacklist(
            user_id=user_id,
            jti=obj_in.jti,
            expired_at=obj_in.expired_at,
            reason=obj_in.reason,
            created_at=datetime.now(timezone.utc),
        )
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Такий токен вже у чорному списку."
            )
        return db_obj

    @staticmethod
    def get(db: Session, blacklist_id: UUID, user_id: UUID) -> TokenBlacklist:
        """
        Отримати запис чорного списку по id (user_id).
        """
        stmt = select(TokenBlacklist).where(
            TokenBlacklist.id == blacklist_id,
            TokenBlacklist.user_id == user_id,
        )
        result = db.execute(stmt).scalar_one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запис не знайдено.")
        return result

    @staticmethod
    def get_by_jti(db: Session, jti: str) -> Optional[TokenBlacklist]:
        """
        Отримати запис по jti (для перевірки блокування токена).
        """
        stmt = select(TokenBlacklist).where(
            TokenBlacklist.jti == jti,
        )
        return db.execute(stmt).scalar_one_or_none()

    @staticmethod
    def get_all(db: Session, user_id: UUID) -> list[TokenBlacklist]:
        """
        Отримати всі записи чорного списку для користувача.
        """
        stmt = (
            select(TokenBlacklist)
            .where(TokenBlacklist.user_id == user_id)
            .order_by(TokenBlacklist.created_at.desc())
        )
        return db.execute(stmt).scalars().all()

    @staticmethod
    def update(
        db: Session, blacklist_id: UUID, user_id: UUID, obj_in: TokenBlacklistUpdate
    ) -> TokenBlacklist:
        """
        Оновити запис чорного списку.
        """
        db_obj = TokenBlacklistCRUD.get(db, blacklist_id, user_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, blacklist_id: UUID, user_id: UUID) -> None:
        """
        Видалити запис чорного списку (повністю).
        """
        db_obj = TokenBlacklistCRUD.get(db, blacklist_id, user_id)
        db.delete(db_obj)
        db.commit()
