from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class DailyProgressBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class DailyProgressCreate(DailyProgressBase):
    pass


class DailyProgressUpdate(DailyProgressBase):
    pass


class DailyProgressRead(DailyProgressBase):
    pass


__all__ = ["DailyProgressBase", "DailyProgressCreate", "DailyProgressUpdate", "DailyProgressRead"]
