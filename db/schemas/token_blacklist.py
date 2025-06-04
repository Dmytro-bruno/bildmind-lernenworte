from typing import Optional

from pydantic import BaseModel

from .user import UserRead


class TokenBlacklistBase(BaseModel):
    user: Optional["UserRead"] = None

    class Config:
        orm_mode = True


class TokenBlacklistCreate(TokenBlacklistBase):
    pass


class TokenBlacklistUpdate(TokenBlacklistBase):
    pass


class TokenBlacklistRead(TokenBlacklistBase):
    pass


__all__ = [
    "TokenBlacklistBase",
    "TokenBlacklistCreate",
    "TokenBlacklistUpdate",
    "TokenBlacklistRead",
]
