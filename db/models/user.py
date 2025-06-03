import uuid

from sqlalchemy import Boolean, Column, DateTime, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from open.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Взаємозв'язки з іншими моделями (додаєш коли реалізуєш ті моделі)
    user_words = relationship("UserWord", back_populates="user", cascade="all, delete-orphan")
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
    test_sessions = relationship("TestSession", back_populates="user", cascade="all, delete-orphan")
    gpt_logs = relationship("GPTLog", back_populates="user", cascade="all, delete-orphan")
    token_blacklist = relationship(
        "TokenBlacklist", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("username", name="uq_user_username"),
    )

    def __repr__(self):
        return f"<User(id={self.id}, " f"email={self.email}, " f"username={self.username}>"
