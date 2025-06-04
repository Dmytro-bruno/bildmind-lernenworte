import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from openapi.db.base import Base


class LevelProgress(Base):
    __tablename__ = "level_progress"
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
    word_level = Column(String(8), nullable=False)  # "A1", "B2", "C2"...
    words_learned = Column(Integer, default=0, nullable=False)
    accuracy = Column(Float, default=0.0, nullable=False)  # Від 0.0 до 1.0 або % (0.0-100.0)
    last_interaction = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)

    # Зв'язки
    user = relationship("User", back_populates="level_progress")

    __table_args__ = (
        UniqueConstraint("user_id", "word_level", name="uq_levelprogress_user_level"),
    )

    def __repr__(self):
        return (
            f"<LevelProgress(id={self.id}, user_id={self.user_id}, word_level={self.word_level}, "
            f"words_learned={self.words_learned}, accuracy={self.accuracy})>"
        )
