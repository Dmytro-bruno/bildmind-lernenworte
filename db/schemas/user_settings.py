from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, constr


class UserSettingsBase(BaseModel):
    """
    Базова схема налаштувань користувача.
    """

    interface_language: constr(min_length=2, max_length=10) = Field(
        "en", description="Мова інтерфейсу (напр. 'en', 'uk', 'de')"
    )
    native_language: constr(min_length=2, max_length=10) = Field(
        "uk", description="Рідна мова користувача (ISO-код)"
    )
    target_language: constr(min_length=2, max_length=10) = Field(
        "de", description="Мова, яку користувач вивчає (ISO-код)"
    )
    notifications_enabled: bool = Field(True, description="Чи увімкнені повідомлення")
    dark_mode: bool = Field(False, description="Чи увімкнений темний режим")


class UserSettingsCreate(UserSettingsBase):
    """
    Схема для створення налаштувань користувача.
    user_id визначається із токена автентифікації.
    """

    pass


class UserSettingsUpdate(BaseModel):
    """
    Схема для часткового оновлення налаштувань користувача.
    """

    interface_language: Optional[constr(min_length=2, max_length=10)] = Field(
        None, description="Нова мова інтерфейсу"
    )
    native_language: Optional[constr(min_length=2, max_length=10)] = Field(
        None, description="Нова рідна мова"
    )
    target_language: Optional[constr(min_length=2, max_length=10)] = Field(
        None, description="Нова мова, яку вивчає користувач"
    )
    notifications_enabled: Optional[bool] = Field(None, description="Оновлений стан повідомлень")
    dark_mode: Optional[bool] = Field(None, description="Оновлений стан темного режиму")
    deleted_at: Optional[datetime] = Field(None, description="Дата видалення налаштувань")


class UserSettingsRead(UserSettingsBase):
    """
    Схема для читання налаштувань користувача (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор налаштувань")
    user_id: UUID = Field(..., description="ID користувача, якому належать налаштування")
    created_at: datetime = Field(..., description="Дата створення запису")
    updated_at: Optional[datetime] = Field(None, description="Дата останнього оновлення")
    deleted_at: Optional[datetime] = Field(
        None, description="Дата видалення (якщо налаштування видалено)"
    )

    class Config:
        orm_mode = True
