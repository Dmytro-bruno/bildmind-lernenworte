from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class UserSettingsBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class UserSettingsCreate(UserSettingsBase):
    pass


class UserSettingsUpdate(UserSettingsBase):
    pass


class UserSettingsRead(UserSettingsBase):
    pass


__all__ = ["UserSettingsBase", "UserSettingsCreate", "UserSettingsUpdate", "UserSettingsRead"]
