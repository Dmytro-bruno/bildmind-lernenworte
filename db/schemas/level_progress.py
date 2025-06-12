from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, confloat, conint, constr


class LevelProgressBase(BaseModel):
    """
    Базова схема прогресу за рівнями знань (A1, B2, C2 тощо).
    """

    word_level: constr(min_length=2, max_length=8) = Field(
        ..., description="Рівень володіння словником (наприклад: 'A1', 'B2', 'C2')"
    )
    words_learned: conint(ge=0) = Field(
        0, description="Кількість вивчених слів на цьому рівні (невід’ємне число)"
    )
    accuracy: confloat(ge=0.0, le=1.0) = Field(
        0.0, description="Точність відповідей (від 0.0 до 1.0)"
    )
    last_interaction: Optional[datetime] = Field(
        None, description="Час останньої взаємодії з цим рівнем"
    )


class LevelProgressCreate(LevelProgressBase):
    """
    Схема для створення запису прогресу за рівнем.
    user_id визначається із токена автентифікації.
    """

    pass


class LevelProgressUpdate(BaseModel):
    """
    Схема для часткового оновлення прогресу (PATCH/PUT).
    """

    words_learned: Optional[conint(ge=0)] = Field(
        None, description="Оновлене значення для кількості вивчених слів"
    )
    accuracy: Optional[confloat(ge=0.0, le=1.0)] = Field(
        None, description="Оновлене значення для точності відповідей"
    )
    last_interaction: Optional[datetime] = Field(
        None, description="Оновлене значення для часу останньої взаємодії"
    )


class LevelProgressRead(LevelProgressBase):
    """
    Схема для читання запису прогресу за рівнем (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор запису")
    user_id: UUID = Field(..., description="ID користувача, якому належить запис")
    created_at: datetime = Field(..., description="Дата створення запису")
    updated_at: Optional[datetime] = Field(None, description="Дата останнього оновлення запису")

    class Config:
        orm_mode = True
