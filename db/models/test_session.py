import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from open.db.base import Base


class TestSession(Base):
    __tablename__ = "test_sessions"

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
    start_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    words_total = Column(Integer, nullable=False)
    correct = Column(Integer, nullable=False)
    test_type = Column(String(50), nullable=False, default="default")
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="test_sessions")

    def __repr__(self):
        return (
            f"<TestSession(id={self.id}, user_id={self.user_id}, "
            f"words_total={self.words_total}, correct={self.correct}, "
            f"start={self.start_time}, end={self.end_time})>"
        )
