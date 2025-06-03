from sqlalchemy import (Boolean, Column, DateTime, Integer, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import relationship

from open.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Взаємозв'язки з іншими моделями (додаєш коли реалізуєш ті моделі)
    user_words = relationship(
        "UserWord", back_populates="user", cascade="all, delete-orphan"
    )
    settings = relationship(
        "UserSettings",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    level_progress = relationship(
        "LevelProgress", back_populates="user", cascade="all, delete-orphan"
    )
    daily_progress = relationship(
        "DailyProgress", back_populates="user", cascade="all, delete-orphan"
    )
    stats = relationship(
        "UserStats",
        uselist=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )
    test_sessions = relationship(
        "TestSession", back_populates="user", cascade="all, delete-orphan"
    )
    gpt_logs = relationship(
        "GPTLog", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("username", name="uq_user_username"),
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"email={self.email}, "
            f"username={self.username}>"
        )
