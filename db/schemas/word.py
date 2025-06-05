from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class WordBase(BaseModel):
    # твої поля
    user_words: Optional[List["UserWordRead"]] = None  # type: ignore[name-defined] # noqa: F821
    gpt_logs: Optional[List["GptLogsRead"]] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class WordCreate(WordBase):
    pass


class WordUpdate(WordBase):
    pass


class WordRead(WordBase):
    pass


__all__ = ["WordBase", "WordCreate", "WordUpdate", "WordRead"]
