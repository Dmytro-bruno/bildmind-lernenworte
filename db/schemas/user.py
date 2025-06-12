from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, constr


# ---------- Базова схема (без id, timestamps і паролів) ----------
class UserBase(BaseModel):
    """
    Базова схема користувача (без службових полів).
    """

    email: EmailStr = Field(..., description="Унікальний email користувача")
    username: constr(min_length=2, max_length=150) = Field(
        ..., description="Унікальне ім'я користувача (логін)"
    )


# ---------- Схема для створення користувача ----------
class UserCreate(UserBase):
    """
    Схема для реєстрації користувача.
    """

    password: constr(min_length=8, max_length=128) = Field(
        ..., description="Пароль користувача (мінімум 8 символів)"
    )


# ---------- Схема для оновлення користувача ----------
class UserUpdate(BaseModel):
    """
    Схема для оновлення даних користувача.
    """

    email: Optional[EmailStr] = Field(None, description="Оновлений email")
    username: Optional[constr(min_length=2, max_length=150)] = Field(
        None, description="Оновлений логін"
    )
    password: Optional[constr(min_length=8, max_length=128)] = Field(
        None, description="Новий пароль"
    )


# ---------- Схема для відповіді (читання) користувача ----------
class UserRead(UserBase):
    """
    Схема для читання (API-відповіді) користувача.
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор користувача")
    is_active: bool = Field(..., description="Чи активний користувач")
    is_superuser: bool = Field(..., description="Чи є користувач адміністратором")
    created_at: Optional[datetime] = Field(None, description="Дата реєстрації")
    updated_at: Optional[datetime] = Field(None, description="Дата останнього оновлення")
    deleted_at: Optional[datetime] = Field(None, description="Дата видалення користувача (якщо є)")

    class Config:
        orm_mode = True


# ---------- Додаткові схеми (тільки для внутрішнього використання, якщо треба) ----------
class UserInDB(UserRead):
    """
    Схема користувача для внутрішньої логіки (включає hashed_password).
    """

    hashed_password: str = Field(..., description="Хеш паролю (тільки для серверної логіки)")
