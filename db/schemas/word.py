from typing import List, Optional

from pydantic import BaseModel, Field

from .gpt_logs import GptLogsRead
from .user_word import UserWordRead


class WordBase(BaseModel):
    user_words: Optional[List[UserWordRead]] = Field(default_factory=list)
    gpt_logs: Optional[List[GptLogsRead]] = Field(default_factory=list)

    class Config:
        orm_mode = True


class WordCreate(WordBase):
    pass


class WordUpdate(WordBase):
    pass


class WordRead(WordBase):
    pass


__all__ = ["WordBase", "WordCreate", "WordUpdate", "WordRead"]
