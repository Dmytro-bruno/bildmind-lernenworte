from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint


class GPTLogBase(BaseModel):
    """
    Базова схема логування GPT-запитів користувача.
    """

    prompt: str = Field(..., description="Вхідний запит (prompt), який відправив користувач")
    response: str = Field(..., description="Відповідь GPT на запит користувача")
    token_usage: conint(ge=0) = Field(0, description="Кількість використаних токенів за сесію")
    word_id: Optional[UUID] = Field(
        None, description="ID слова, до якого належить запит (опціонально)"
    )


class GPTLogCreate(GPTLogBase):
    """
    Схема для створення лог-запису GPT.
    user_id визначається із токена автентифікації.
    """

    pass


class GPTLogUpdate(BaseModel):
    """
    Схема для оновлення лог-запису GPT (допускаються лише окремі поля).
    """

    prompt: Optional[str] = Field(None, description="Оновлений prompt")
    response: Optional[str] = Field(None, description="Оновлена відповідь GPT")
    token_usage: Optional[conint(ge=0)] = Field(
        None, description="Оновлена кількість використаних токенів"
    )
    word_id: Optional[UUID] = Field(None, description="Оновлений word_id")


class GPTLogRead(GPTLogBase):
    """
    Схема для читання лог-запису GPT (API-відповідь).
    """

    id: UUID = Field(..., description="Унікальний ідентифікатор лог-запису")
    user_id: UUID = Field(..., description="ID користувача, який зробив запит")
    timestamp: datetime = Field(..., description="Час створення лог-запису (UTC)")

    class Config:
        orm_mode = True
