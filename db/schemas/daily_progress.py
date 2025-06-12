from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint


class DailyProgressBase(BaseModel):
    """
    Базова схема щоденного прогресу користувача.
    Використовується як основа для створення та оновлення запису.
    """

    date: datetime = Field(
        ..., description="Дата дня, для якого зберігається прогрес (у форматі ISO 8601)"
    )
    words_learned: conint(ge=0) = Field(
        0, description="Кількість вивчених слів за цей день (невід’ємне число)"
    )
    words_reviewed: conint(ge=0) = Field(
        0, description="Кількість повторених слів за цей день (невід’ємне число)"
    )
    test_sessions_passed: conint(ge=0) = Field(
        0, description="Кількість пройдених тестових сесій за цей день (невід’ємне число)"
    )


class DailyProgressCreate(DailyProgressBase):
    """
    Схема для створення запису щоденного прогресу.
    user_id визначається із токена автентифікації.
    """

    pass


class DailyProgressUpdate(BaseModel):
    """
    Схема для часткового оновлення прогресу (тільки ті поля, які змінюються).
    """

    words_learned: Optional[conint(ge=0)] = Field(
        None, description="Оновлене значення для вивчених слів"
    )
    words_reviewed: Optional[conint(ge=0)] = Field(
        None, description="Оновлене значення для повторених слів"
    )
    test_sessions_passed: Optional[conint(ge=0)] = Field(
        None, description="Оновлене значення для тестових сесій"
    )


class DailyProgressRead(DailyProgressBase):
    """
    Схема для читання запису прогресу (те, що повертається у відповідях API).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор запису")
    user_id: UUID = Field(..., description="Ідентифікатор користувача")
    created_at: datetime = Field(..., description="Дата та час створення запису")
    updated_at: Optional[datetime] = Field(
        None, description="Дата та час останнього оновлення запису"
    )
    deleted_at: Optional[datetime] = Field(None, description="Дата видалення (якщо запис видалено)")

    class Config:
        orm_mode = True
