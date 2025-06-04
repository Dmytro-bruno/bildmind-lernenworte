from typing import Optional

from pydantic import BaseModel

from .user import UserRead


class TestSessionBase(BaseModel):
    user: Optional["UserRead"] = None

    class Config:
        orm_mode = True


class TestSessionCreate(TestSessionBase):
    pass


class TestSessionUpdate(TestSessionBase):
    pass


class TestSessionRead(TestSessionBase):
    pass


__all__ = ["TestSessionBase", "TestSessionCreate", "TestSessionUpdate", "TestSessionRead"]
