from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class TestSessionBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class TestSessionCreate(TestSessionBase):
    pass


class TestSessionUpdate(TestSessionBase):
    pass


class TestSessionRead(TestSessionBase):
    pass


__all__ = ["TestSessionBase", "TestSessionCreate", "TestSessionUpdate", "TestSessionRead"]
