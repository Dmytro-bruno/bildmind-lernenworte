from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, constr


class WordBase(BaseModel):
    """
    Базова схема слова (для додавання і редагування).
    """

    base_form: constr(min_length=1, max_length=255) = Field(
        ..., description="Початкова форма слова (без артикля)"
    )
    article: Optional[constr(max_length=10)] = Field(
        None, description="Артикль (напр., 'der', 'die', 'das')"
    )
    base_and_article: constr(min_length=1, max_length=255) = Field(
        ..., description="Форма слова з артиклем"
    )
    translation: constr(min_length=1, max_length=255) = Field(..., description="Переклад слова")
    lang_from: constr(min_length=2, max_length=10) = Field(
        ..., description="Мова оригіналу (ISO-код, напр. 'de', 'en')"
    )
    lang_to: constr(min_length=2, max_length=10) = Field(
        ..., description="Мова перекладу (ISO-код, напр. 'uk', 'en')"
    )
    example: Optional[constr(max_length=512)] = Field(
        None, description="Приклад вживання слова (опціонально)"
    )


class WordCreate(WordBase):
    """
    Схема для створення слова у словнику.
    """

    pass


class WordUpdate(BaseModel):
    """
    Схема для часткового оновлення даних слова.
    """

    base_form: Optional[constr(min_length=1, max_length=255)] = Field(
        None, description="Оновлена початкова форма слова"
    )
    article: Optional[constr(max_length=10)] = Field(None, description="Оновлений артикль")
    base_and_article: Optional[constr(min_length=1, max_length=255)] = Field(
        None, description="Оновлена форма слова з артиклем"
    )
    translation: Optional[constr(min_length=1, max_length=255)] = Field(
        None, description="Оновлений переклад"
    )
    lang_from: Optional[constr(min_length=2, max_length=10)] = Field(
        None, description="Оновлена мова оригіналу"
    )
    lang_to: Optional[constr(min_length=2, max_length=10)] = Field(
        None, description="Оновлена мова перекладу"
    )
    example: Optional[constr(max_length=512)] = Field(
        None, description="Оновлений приклад вживання"
    )


class WordRead(WordBase):
    """
    Схема для читання слова (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор слова")
    created_at: datetime = Field(..., description="Дата створення слова")
    deleted_at: Optional[datetime] = Field(None, description="Дата видалення (якщо застосовано)")

    class Config:
        orm_mode = True
