from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, constr


class TokenBlacklistBase(BaseModel):
    """
    Базова схема для внесення JWT у чорний список (Token Blacklist).
    """

    jti: constr(min_length=8, max_length=128) = Field(
        ..., description="Унікальний ідентифікатор JWT (jti)"
    )
    expired_at: datetime = Field(..., description="Час, до якого токен заблоковано (UTC)")
    reason: Optional[constr(max_length=100)] = Field(
        None, description="Причина блокування токена (опціонально)"
    )


class TokenBlacklistCreate(TokenBlacklistBase):
    """
    Схема для додавання токена у чорний список.
    user_id визначається із токена автентифікації.
    """

    pass


class TokenBlacklistUpdate(BaseModel):
    """
    Схема для оновлення запису у чорному списку (якщо це потрібно).
    """

    expired_at: Optional[datetime] = Field(None, description="Оновлений час блокування")
    reason: Optional[constr(max_length=100)] = Field(
        None, description="Оновлена причина блокування токена"
    )


class TokenBlacklistRead(TokenBlacklistBase):
    """
    Схема для читання запису з чорного списку (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор запису")
    user_id: UUID = Field(..., description="ID користувача, якому належить токен")
    created_at: datetime = Field(..., description="Час додавання токена у чорний список (UTC)")

    class Config:
        orm_mode = True
