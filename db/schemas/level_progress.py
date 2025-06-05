from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class LevelProgressBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class LevelProgressCreate(LevelProgressBase):
    pass


class LevelProgressUpdate(LevelProgressBase):
    pass


class LevelProgressRead(LevelProgressBase):
    pass


__all__ = ["LevelProgressBase", "LevelProgressCreate", "LevelProgressUpdate", "LevelProgressRead"]
