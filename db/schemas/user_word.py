from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class UserWordBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821
    word: Optional["WordRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class UserWordCreate(UserWordBase):
    pass


class UserWordUpdate(UserWordBase):
    pass


class UserWordRead(UserWordBase):
    pass


__all__ = ["UserWordBase", "UserWordCreate", "UserWordUpdate", "UserWordRead"]
