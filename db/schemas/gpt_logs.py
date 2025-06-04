from typing import Optional

from pydantic import BaseModel

from .user import UserRead
from .word import WordRead


class GptLogsBase(BaseModel):
    user: Optional["UserRead"] = None
    word: Optional["WordRead"] = None

    class Config:
        orm_mode = True


class GptLogsCreate(GptLogsBase):
    pass


class GptLogsUpdate(GptLogsBase):
    pass


class GptLogsRead(GptLogsBase):
    pass


__all__ = ["GptLogsBase", "GptLogsCreate", "GptLogsUpdate", "GptLogsRead"]
