from .daily_progress import (
    DailyProgressBase,
    DailyProgressCreate,
    DailyProgressRead,
    DailyProgressUpdate,
)
from .gpt_logs import GptLogsBase, GptLogsCreate, GptLogsRead, GptLogsUpdate
from .level_progress import (
    LevelProgressBase,
    LevelProgressCreate,
    LevelProgressRead,
    LevelProgressUpdate,
)
from .test_session import TestSessionBase, TestSessionCreate, TestSessionRead, TestSessionUpdate
from .token_blacklist import (
    TokenBlacklistBase,
    TokenBlacklistCreate,
    TokenBlacklistRead,
    TokenBlacklistUpdate,
)
from .user import UserBase, UserCreate, UserRead, UserUpdate
from .user_settings import (
    UserSettingsBase,
    UserSettingsCreate,
    UserSettingsRead,
    UserSettingsUpdate,
)
from .user_stats import UserStatsBase, UserStatsCreate, UserStatsRead, UserStatsUpdate
from .user_word import UserWordBase, UserWordCreate, UserWordRead, UserWordUpdate
from .word import WordBase, WordCreate, WordRead, WordUpdate

UserBase.model_rebuild()
UserCreate.model_rebuild()
UserUpdate.model_rebuild()
UserRead.model_rebuild()
WordBase.model_rebuild()
WordCreate.model_rebuild()
WordUpdate.model_rebuild()
WordRead.model_rebuild()
UserWordBase.model_rebuild()
UserWordCreate.model_rebuild()
UserWordUpdate.model_rebuild()
UserWordRead.model_rebuild()
LevelProgressBase.model_rebuild()
LevelProgressCreate.model_rebuild()
LevelProgressUpdate.model_rebuild()
LevelProgressRead.model_rebuild()
DailyProgressBase.model_rebuild()
DailyProgressCreate.model_rebuild()
DailyProgressUpdate.model_rebuild()
DailyProgressRead.model_rebuild()
UserSettingsBase.model_rebuild()
UserSettingsCreate.model_rebuild()
UserSettingsUpdate.model_rebuild()
UserSettingsRead.model_rebuild()
UserStatsBase.model_rebuild()
UserStatsCreate.model_rebuild()
UserStatsUpdate.model_rebuild()
UserStatsRead.model_rebuild()
TestSessionBase.model_rebuild()
TestSessionCreate.model_rebuild()
TestSessionUpdate.model_rebuild()
TestSessionRead.model_rebuild()
GptLogsBase.model_rebuild()
GptLogsCreate.model_rebuild()
GptLogsUpdate.model_rebuild()
GptLogsRead.model_rebuild()
TokenBlacklistBase.model_rebuild()
TokenBlacklistCreate.model_rebuild()
TokenBlacklistUpdate.model_rebuild()
TokenBlacklistRead.model_rebuild()
