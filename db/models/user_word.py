import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from openapi.db.base import Base


class UserWord(Base):
    __tablename__ = "user_words"
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
    word_id = Column(
        UUID(as_uuid=True),
        ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # ───── SM-2 fields ─────
    easiness_factor = Column(
        Float,
        nullable=False,
        server_default=text("2.5"),
    )
    repetition = Column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )
    interval = Column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )
    # ───────────────────────
    level = Column(Integer, nullable=False, default=0)
    next_review_date = Column(DateTime(timezone=True), nullable=True)
    last_review_date = Column(DateTime(timezone=True), nullable=True)
    is_learned = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    # Додані поля для аналітики й нотаток
    success_count = Column(Integer, default=0, nullable=False)
    fail_count = Column(Integer, default=0, nullable=False)
    note = Column(String, nullable=True)

    # Зв'язки
    user = relationship("User", back_populates="user_words")
    word = relationship("Word", back_populates="user_words")

    __table_args__ = (UniqueConstraint("user_id", "word_id", name="uq_userword_user_word"),)

    def __repr__(self):
        return (
            f"<UserWord(id={self.id}, user_id={self.user_id}, word_id={self.word_id}, "
            f"level={self.level}, is_learned={self.is_learned}, "
            f"ef={self.easiness_factor}, rep={self.repetition}, intv={self.interval})>"
        )
