from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint

from .word import WordRead


class UserWordBase(BaseModel):
    """
    Базова схема зв'язку слова з користувачем (статус вивчення, рівень, аналітика).
    """

    word_id: UUID = Field(..., description="ID слова в загальному словнику")
    level: conint(ge=0) = Field(
        0, description="Поточний рівень слова для користувача (інтервал або стадія)"
    )
    next_review_date: Optional[datetime] = Field(
        None, description="Дата наступного повторення слова (UTC)"
    )
    last_review_date: Optional[datetime] = Field(
        None, description="Дата останнього повторення слова (UTC)"
    )
    is_learned: bool = Field(False, description="Чи вважається слово вивченим")
    success_count: conint(ge=0) = Field(
        0, description="Кількість вдалих відповідей користувача по слову"
    )
    fail_count: conint(ge=0) = Field(0, description="Кількість невдалих спроб по слову")
    note: Optional[str] = Field(None, description="Нотатка до слова (опціонально)")


class UserWordCreate(UserWordBase):
    """
    Схема для додавання слова до словника користувача.
    user_id визначається із токена автентифікації.
    """

    pass


class UserWordUpdate(BaseModel):
    """
    Схема для часткового оновлення статусу слова у користувача.
    """

    level: Optional[conint(ge=0)] = Field(None, description="Оновлений рівень слова")
    next_review_date: Optional[datetime] = Field(
        None, description="Оновлена дата наступного повторення"
    )
    last_review_date: Optional[datetime] = Field(
        None, description="Оновлена дата останнього повторення"
    )
    is_learned: Optional[bool] = Field(None, description="Оновлений статус вивченості слова")
    success_count: Optional[conint(ge=0)] = Field(
        None, description="Оновлена кількість успішних відповідей"
    )
    fail_count: Optional[conint(ge=0)] = Field(
        None, description="Оновлена кількість невдалих спроб"
    )
    note: Optional[str] = Field(None, description="Оновлена нотатка до слова")
    deleted_at: Optional[datetime] = Field(
        None, description="Дата видалення зв'язку (якщо застосовано)"
    )


class UserWordRead(UserWordBase):
    """
    Схема для читання зв'язку користувача і слова (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор зв'язку користувача і слова")
    user_id: UUID = Field(..., description="ID користувача, якому належить слово")
    created_at: datetime = Field(..., description="Дата додавання слова до словника")
    updated_at: Optional[datetime] = Field(None, description="Дата останнього оновлення")
    deleted_at: Optional[datetime] = Field(
        None, description="Дата видалення зв'язку (якщо застосовано)"
    )
    word: WordRead = Field(..., description="Повна інформація про слово")

    class Config:
        orm_mode = True
