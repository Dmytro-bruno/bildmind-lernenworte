import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base import Base


class UserStats(Base):
    __tablename__ = "user_stats"

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
        unique=True,
        nullable=False,
    )
    words_learned = Column(Integer, nullable=False, default=0)
    words_in_progress = Column(Integer, nullable=False, default=0)
    test_sessions_total = Column(Integer, nullable=False, default=0)
    test_sessions_passed = Column(Integer, nullable=False, default=0)
    last_active = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="stats")

    __table_args__ = (UniqueConstraint("user_id", name="uq_user_stats_user_id"),)

    def __repr__(self):
        return (
            f"<UserStats(id={self.id}, user_id={self.user_id}, words_learned={self.words_learned})>"
        )
