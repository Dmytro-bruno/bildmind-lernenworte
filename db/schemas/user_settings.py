from typing import Optional

from pydantic import BaseModel

from .user import UserRead


class UserSettingsBase(BaseModel):
    user: Optional["UserRead"] = None

    class Config:
        orm_mode = True


class UserSettingsCreate(UserSettingsBase):
    pass


class UserSettingsUpdate(UserSettingsBase):
    pass


class UserSettingsRead(UserSettingsBase):
    pass


__all__ = ["UserSettingsBase", "UserSettingsCreate", "UserSettingsUpdate", "UserSettingsRead"]
