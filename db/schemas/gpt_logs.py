from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class GptLogsBase(BaseModel):
    # твої поля
    user: Optional["UserRead"] = None  # type: ignore[name-defined] # noqa: F821
    word: Optional["WordRead"] = None  # type: ignore[name-defined] # noqa: F821

    class Config:
        from_attributes = True


class GptLogsCreate(GptLogsBase):
    pass


class GptLogsUpdate(GptLogsBase):
    pass


class GptLogsRead(GptLogsBase):
    pass


__all__ = ["GptLogsBase", "GptLogsCreate", "GptLogsUpdate", "GptLogsRead"]
