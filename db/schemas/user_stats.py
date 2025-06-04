from typing import Optional

from pydantic import BaseModel

from .user import UserRead


class UserStatsBase(BaseModel):
    user: Optional["UserRead"] = None

    class Config:
        orm_mode = True


class UserStatsCreate(UserStatsBase):
    pass


class UserStatsUpdate(UserStatsBase):
    pass


class UserStatsRead(UserStatsBase):
    pass


__all__ = ["UserStatsBase", "UserStatsCreate", "UserStatsUpdate", "UserStatsRead"]
