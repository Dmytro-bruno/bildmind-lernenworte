from typing import Optional

from pydantic import BaseModel

from .user import UserRead
from .word import WordRead


class UserWordBase(BaseModel):
    user: Optional["UserRead"] = None
    word: Optional["WordRead"] = None

    class Config:
        orm_mode = True


class UserWordCreate(UserWordBase):
    pass


class UserWordUpdate(UserWordBase):
    pass


class UserWordRead(UserWordBase):
    pass


__all__ = ["UserWordBase", "UserWordCreate", "UserWordUpdate", "UserWordRead"]
