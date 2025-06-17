from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Тип токену (bearer)")


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email користувача")
    password: str = Field(..., description="Пароль користувача")


class TokenPayload(BaseModel):
    sub: str = Field(..., description="ID користувача (user_id)")
    exp: datetime = Field(..., description="Дата закінчення токену (expiration)")
    jti: UUID = Field(..., description="Унікальний ідентифікатор токену (JWT ID)")
