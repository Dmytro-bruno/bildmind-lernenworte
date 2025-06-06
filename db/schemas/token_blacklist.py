from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class TokenBlacklistBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


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
