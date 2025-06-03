import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base import Base


class DailyProgress(Base):
    __tablename__ = "daily_progress"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = Column(
        DateTime(timezone=True), nullable=False, index=True
    )  # Дата дня, для якого зберігається прогрес
    words_learned = Column(Integer, default=0, nullable=False)
    words_reviewed = Column(Integer, default=0, nullable=False)
    test_sessions_passed = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Зв’язок з User
    user = relationship("User", back_populates="daily_progress")

    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_daily_progress_user_date"),)

    def __repr__(self):
        return (
            f"<DailyProgress(id={self.id}, "
            f"user_id={self.user_id}, date={self.date}, "
            f"words_learned={self.words_learned})>"
        )
