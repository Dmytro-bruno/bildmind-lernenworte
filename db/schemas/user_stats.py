from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class UserStatsBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class UserStatsCreate(UserStatsBase):
    pass


class UserStatsUpdate(UserStatsBase):
    pass


class UserStatsRead(UserStatsBase):
    pass


__all__ = ["UserStatsBase", "UserStatsCreate", "UserStatsUpdate", "UserStatsRead"]
