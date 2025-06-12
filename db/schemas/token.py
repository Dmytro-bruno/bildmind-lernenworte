from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Тип токену (bearer)")


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email користувача")
    password: str = Field(..., description="Пароль користувача")
