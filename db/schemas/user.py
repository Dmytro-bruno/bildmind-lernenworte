from typing import List, Optional

from pydantic import BaseModel, Field

from .daily_progress import DailyProgressRead
from .gpt_logs import GptLogsRead
from .level_progress import LevelProgressRead
from .test_session import TestSessionRead
from .token_blacklist import TokenBlacklistRead
from .user_settings import UserSettingsRead
from .user_stats import UserStatsRead
from .user_word import UserWordRead


class UserBase(BaseModel):
    user_words: Optional[List[UserWordRead]] = Field(default_factory=list)
    settings: Optional[UserSettingsRead] = None
    level_progress: List[LevelProgressRead] = Field(default_factory=list)
    daily_progress: List[DailyProgressRead] = Field(default_factory=list)
    stats: Optional[UserStatsRead] = None
    test_sessions: List[TestSessionRead] = Field(default_factory=list)
    gpt_logs: List[GptLogsRead] = Field(default_factory=list)
    token_blacklist: List[TokenBlacklistRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    pass


__all__ = ["UserBase", "UserCreate", "UserUpdate", "UserRead"]
