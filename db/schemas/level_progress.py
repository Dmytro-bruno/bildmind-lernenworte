from typing import Optional

from pydantic import BaseModel

from .user import UserRead


class LevelProgressBase(BaseModel):
    user: Optional["UserRead"] = None

    class Config:
        orm_mode = True


class LevelProgressCreate(LevelProgressBase):
    pass


class LevelProgressUpdate(LevelProgressBase):
    pass


class LevelProgressRead(LevelProgressBase):
    pass


__all__ = ["LevelProgressBase", "LevelProgressCreate", "LevelProgressUpdate", "LevelProgressRead"]
