from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint


class UserStatsBase(BaseModel):
    """
    Базова схема статистики користувача.
    """

    words_learned: conint(ge=0) = Field(0, description="Загальна кількість вивчених слів")
    words_in_progress: conint(ge=0) = Field(0, description="Кількість слів у процесі вивчення")
    test_sessions_total: conint(ge=0) = Field(0, description="Загальна кількість тестових сесій")
    test_sessions_passed: conint(ge=0) = Field(
        0, description="Кількість успішно пройдених тестових сесій"
    )
    last_active: Optional[datetime] = Field(
        None, description="Час останньої активності користувача"
    )


class UserStatsCreate(UserStatsBase):
    """
    Схема для створення статистики користувача.
    user_id визначається із токена автентифікації.
    """

    pass


class UserStatsUpdate(BaseModel):
    """
    Схема для часткового оновлення статистики користувача.
    """

    words_learned: Optional[conint(ge=0)] = Field(
        None, description="Оновлена кількість вивчених слів"
    )
    words_in_progress: Optional[conint(ge=0)] = Field(
        None, description="Оновлена кількість слів у процесі"
    )
    test_sessions_total: Optional[conint(ge=0)] = Field(
        None, description="Оновлена кількість тестових сесій"
    )
    test_sessions_passed: Optional[conint(ge=0)] = Field(
        None, description="Оновлена кількість успішних тестів"
    )
    last_active: Optional[datetime] = Field(None, description="Оновлений час останньої активності")
    deleted_at: Optional[datetime] = Field(
        None, description="Дата видалення статистики (якщо застосовано)"
    )


class UserStatsRead(UserStatsBase):
    """
    Схема для читання статистики користувача (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор статистики")
    user_id: UUID = Field(..., description="ID користувача, до якого належить статистика")
    created_at: datetime = Field(..., description="Дата створення запису")
    updated_at: Optional[datetime] = Field(None, description="Дата останнього оновлення")
    deleted_at: Optional[datetime] = Field(None, description="Дата видалення (якщо застосовано)")

    class Config:
        orm_mode = True
