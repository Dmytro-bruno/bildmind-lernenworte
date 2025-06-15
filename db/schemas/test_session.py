from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint, constr


class TestSessionBase(BaseModel):
    """
    Базова схема сесії тестування користувача.
    """

    start_time: datetime = Field(..., description="Час початку тестової сесії (UTC)")
    end_time: datetime = Field(..., description="Час завершення тестової сесії (UTC)")
    words_total: conint(ge=1) = Field(
        ..., description="Загальна кількість слів у тесті (мінімум 1)"
    )
    correct: conint(ge=0) = Field(
        ..., description="Кількість правильних відповідей (невід’ємне число)"
    )
    test_type: constr(min_length=1, max_length=50) = Field(
        "default", description="Тип тестової сесії (наприклад, 'default', 'listening', 'writing')"
    )


class TestSessionCreate(TestSessionBase):
    """
    Схема для створення сесії тестування.
    user_id визначається із токена автентифікації.
    """

    user_id: UUID = Field(..., description="ID користувача, якому належить сесія")


class TestSessionUpdate(BaseModel):
    """
    Схема для часткового оновлення сесії тестування.
    """

    end_time: Optional[datetime] = Field(None, description="Оновлений час завершення тесту")
    words_total: Optional[conint(ge=1)] = Field(
        None, description="Оновлене значення загальної кількості слів"
    )
    correct: Optional[conint(ge=0)] = Field(
        None, description="Оновлене значення кількості правильних відповідей"
    )
    test_type: Optional[constr(min_length=1, max_length=50)] = Field(
        None, description="Оновлений тип тестової сесії"
    )
    deleted_at: Optional[datetime] = Field(None, description="Дата видалення (якщо запис видалено)")


class TestSessionRead(TestSessionBase):
    """
    Схема для читання сесії тестування (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор сесії тестування")
    user_id: UUID = Field(..., description="ID користувача, якому належить сесія")
    deleted_at: Optional[datetime] = Field(None, description="Дата видалення (якщо запис видалено)")

    class Config:
        orm_mode = True
