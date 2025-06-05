from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    ...
    daily_progress: Optional[List["DailyProgressRead"]] = None  # type: ignore[name-defined] # noqa: F821, E501
    level_progress: Optional[List["LevelProgressRead"]] = None  # type: ignore[name-defined] # noqa: F821, E501
    user_words: Optional[List["UserWordRead"]] = None  # type: ignore[name-defined] # noqa: F821, E501
    user_settings: Optional["UserSettingsRead"] = None  # type: ignore[name-defined] # noqa: F821, E501
    user_stats: Optional["UserStatsRead"] = None  # type: ignore[name-defined] # noqa: F821, E501
    test_sessions: Optional[List["TestSessionRead"]] = None  # type: ignore[name-defined] # noqa: F821, E501
    gpt_logs: Optional[List["GptLogsRead"]] = None  # type: ignore[name-defined] # noqa: F821, E501
    token_blacklist: Optional[List["TokenBlacklistRead"]] = None  # type: ignore[name-defined] # noqa: F821, E501

    ...

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    pass


__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserRead"]
