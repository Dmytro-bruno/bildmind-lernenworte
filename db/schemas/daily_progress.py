from typing import Optional

from pydantic import BaseModel

from .user import UserRead


class DailyProgressBase(BaseModel):
    user: Optional["UserRead"] = None

    class Config:
        orm_mode = True


class DailyProgressCreate(DailyProgressBase):
    pass


class DailyProgressUpdate(DailyProgressBase):
    pass


class DailyProgressRead(DailyProgressBase):
    pass


__all__ = ["DailyProgressBase", "DailyProgressCreate", "DailyProgressUpdate", "DailyProgressRead"]
